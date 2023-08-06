from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, List

import pandas as pd
import sqlalchemy as sa
from colassigner.constants import PREFIX_SEP
from sqlalchemy.orm import sessionmaker
from structlog import get_logger

from ..config_loading import RunConfig
from ..get_runtime import get_runtime
from ..metadata.atoms import EntityClass, feats_to_cols, to_sa_col
from ..metadata.high_level import NamespaceMetadata
from ..metadata.scrutable import ScruTable
from ..utils import is_postgres

if TYPE_CHECKING:
    from ..project_runtime import ProjectRuntime  # pragma: no cover


logger = get_logger(ctx="sql loader")


class SqlLoader:
    """loads an entire project environment to an sql database

    metadata needs to be serialized

    """

    def __init__(self, constr, echo=False, batch_size=2000):
        """start up a loader

        Parameters
        ----------
        constr : str, optional
            constring where database is found, by default "sqlite:///:memory:"
            but needs to be postgres for foreign keys to be validated
        """

        self.runtime = get_runtime()
        self.engine = sa.create_engine(constr, echo=echo)
        self.sql_meta = sa.MetaData()
        self._Session = sessionmaker(self.engine)
        self._batch_size = batch_size

    def setup_schema(self):
        for nsm in self._get_ns_mappers(False):
            nsm.create_schema()
        self.sql_meta.create_all(bind=self.engine)

    def load_data(self, env):
        with RunConfig(read_env=env):
            with self._Session() as session:
                for nsm in self._get_ns_mappers():
                    nsm.load_data(session)
                session.commit()

    def validate_data(self, env):
        with RunConfig(read_env=env):
            for nsm in self._get_ns_mappers():
                nsm.validate_data()

    def purge(self):
        self.sql_meta.drop_all(bind=self.engine)

    def _get_ns_mappers(self, data_only=True):
        f_args = (self.runtime, self.sql_meta, self.engine, self._batch_size)
        _mapped = set()
        for ns in self.runtime.metadata.namespaces.values():
            _mapped.add((self.runtime.name, ns.name))
            yield NamespaceMapper(self.runtime.name, ns, *f_args)
        for data_env in self.runtime.data_to_load:
            proj_name, ext_ns_name = _id = (data_env.project, data_env.ns)
            ext_ns = self.runtime.metadata_dic[proj_name].namespaces[ext_ns_name]
            if _id in _mapped:
                continue
            _mapped.add(_id)
            yield NamespaceMapper(proj_name, ext_ns, *f_args)
        if data_only:
            return
        for proj_name, ext_proj in self.runtime.metadata_dic.items():
            for ns in ext_proj.namespaces.values():
                _id = (proj_name, ns.name)
                if _id in _mapped:
                    continue
                _mapped.add(_id)
                yield NamespaceMapper(proj_name, ns, *f_args)


@dataclass
class NamespaceMapper:
    project_name: str
    ns_meta: NamespaceMetadata
    runtime: "ProjectRuntime"
    sql_meta: sa.MetaData
    engine: sa.engine.Engine
    batch_size: int

    def create_schema(self):
        for table in self.ns_meta.tables:
            SqlTableConverter(table, self).create()

    def load_data(self, session):
        for table in self.ns_meta.tables:
            self._load_table(table, session)

    def validate_data(self):
        for table in self.ns_meta.tables:
            self._validate_table(table)

    def _load_table(self, table: ScruTable, session):
        ins = self.sql_meta.tables[table.id_.sql_id].insert()
        logger.info("loading", table=table.id_.sql_id)
        for df in table.dfs:
            self._partition(df.reset_index() if table.index else df, ins, session)

    def _validate_table(self, table: ScruTable):
        dt_map = {}
        table_id = table.id_.sql_id
        logger.info("validating table", table=table_id)
        if not is_postgres(self.engine):
            dt_map = table.dtype_map
        df_sql = pd.read_sql(f"SELECT * FROM {table_id}", con=self.engine).astype(
            dt_map
        )
        df = table.get_full_df()
        if table.index:
            ind_cols = table.index_cols
            if len(ind_cols) > 1:
                ind_cols = [ind_cols[ind_cols.index(inc)] for inc in df.index.names]
            df_sql = df_sql.set_index(ind_cols).reindex(df.index)
        else:
            df, df_sql = [
                _df.sort_values(df_sql.columns.tolist()).reset_index(drop=True)
                for _df in [df, df_sql]
            ]
        if df.empty and df_sql.empty:
            logger.warning("empty data frames", table=table_id)

        pd.testing.assert_frame_equal(df.loc[:, df_sql.columns], df_sql)

    def _partition(self, df: pd.DataFrame, ins, session):
        for sind in range(0, df.shape[0], self.batch_size):
            eind = sind + self.batch_size
            recs = df.iloc[sind:eind, :].to_dict("records")
            session.execute(ins.values([*map(_parse_d, recs)]))


class SqlTableConverter:
    def __init__(self, scrutable: ScruTable, parent_mapper: NamespaceMapper):
        self._table = scrutable
        self._mapper = parent_mapper
        self._sql_id = scrutable.id_.sql_id
        self.fk_constraints = []
        self.ind_cols = self._get_sa_cols(scrutable.index, True)
        self.feat_cols = self._get_sa_cols(scrutable.features, False)

    def create(self):
        sa.Table(
            self._sql_id,
            self._mapper.sql_meta,
            *self._schema_items,
        )

    def _add_fk(
        self,
        sql_cols: List[sa.Column],
        entity: EntityClass,
        prefix_arr,
    ):
        target_table = self._mapper.runtime.get_table_for_entity(
            entity, self._table, prefix_arr
        )
        pref_str = PREFIX_SEP.join(prefix_arr) + PREFIX_SEP
        matching_cols = [
            c.name.replace(pref_str, f"{target_table.id_.sql_id}.") for c in sql_cols
        ]
        defer_kws = {}
        if is_postgres(self._mapper.engine):
            defer_kws["initially"] = "DEFERRED"

        fk = sa.ForeignKeyConstraint(
            sql_cols,
            matching_cols,
            name=f"_{self._sql_id}_{pref_str}_fk",
            **defer_kws,
        )
        self.fk_constraints.append(fk)

    def _get_sa_cols(self, feats, pk):
        return feats_to_cols(feats, self._add_fk, partial(to_sa_col, pk=pk))

    @property
    def _schema_items(self):
        return [
            *self.feat_cols,
            *self.ind_cols,
            *self.fk_constraints,
        ]


@contextmanager
def tmp_constr(v=False):
    sqlpath = Path("__tmp.db")
    constr = f"sqlite:///{sqlpath.name}"
    loader = SqlLoader(constr, echo=v)
    try:
        loader.setup_schema()
        yield constr
    finally:
        loader.purge()
        sqlpath.unlink()


def _parse_d(d):
    return {k: None if pd.isna(v) else v for k, v in d.items()}
