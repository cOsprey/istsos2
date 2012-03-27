#=============================================
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

#=============================================
#this need to ba added to make it work out!!!!
#=============================================
from sqlalchemy.dialects import postgresql
from sqlalchemy.types import NullType, TypeDecorator
from geoalchemy import *
from geoalchemy.postgis import PGComparator
#=============================================

engine = create_engine('postgresql+psycopg2://sos:sos@localhost/sostest',echo=True)
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

try:
    from sqlalchemy.dialects.postgresql import *
except ImportError:
    from sqlalchemy.databases.postgres import *

"""
geom_foi = GeometryColumn(u'geom_foi',Geometry(), comparator=PGComparator)
GeometryDDL(Foi.__table__)
"""

    
measures = Table(u'measures', metadata,
    Column(u'id_msr', BIGINT(), primary_key=True, nullable=False),
    Column(u'id_eti_fk', BIGINT(), ForeignKey('event_time.id_eti'), nullable=False),
    Column(u'id_qi_fk', INTEGER(), ForeignKey('quality_index.id_qi'), nullable=False),
    Column(u'id_opr_fk', INTEGER(), ForeignKey('observed_properties.id_opr'), nullable=False),
    Column(u'val_msr', NUMERIC(precision=10, scale=6), nullable=False),
)

off_proc = Table(u'off_proc', metadata,
    Column(u'id_off_prc', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_off_fk', INTEGER(), ForeignKey('offerings.id_off'), nullable=False),
    Column(u'id_prc_fk', INTEGER(), ForeignKey('procedures.id_prc'), nullable=False),
)


positions = Table(u'positions', metadata,
    Column(u'id_pos', BIGINT(), primary_key=True, nullable=False),
    Column(u'id_qi_fk', INTEGER(), ForeignKey('quality_index.id_qi'), nullable=False),
    Column(u'geom_pos',Point(2,21781),nullable=False),
    #Column(u'geom_pos', NullType(), nullable=False),
    Column(u'id_eti_fk', BIGINT(), ForeignKey('event_time.id_eti'), nullable=False),
)

GeometryDDL(positions)

proc_obs = Table(u'proc_obs', metadata,
    Column(u'id_pro', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_prc_fk', INTEGER(), ForeignKey('procedures.id_prc'), nullable=False),
    Column(u'id_uom_fk', INTEGER(), ForeignKey('uoms.id_uom'), nullable=False),
    Column(u'id_opr_fk', INTEGER(), ForeignKey('observed_properties.id_opr'), nullable=False),
)

procedures = Table(u'procedures', metadata,
    Column(u'name_prc', VARCHAR(length=30), nullable=False),
    Column(u'desc_prc', TEXT()),
    Column(u'stime_prc', TIMESTAMP(timezone=True)),
    Column(u'etime_prc', TIMESTAMP(timezone=True)),
    Column(u'id_prc', INTEGER(), primary_key=True, nullable=False),
    Column(u'id_tru_fk', INTEGER(), ForeignKey('time_res_unit.id_tru'), nullable=False),
    Column(u'time_res_prc', INTEGER()),
    Column(u'id_oty_fk', INTEGER(), ForeignKey('obs_type.id_oty')),
    Column(u'id_foi_fk', INTEGER(), ForeignKey('foi.id_foi')),
    Column(u'assignedid_prc', VARCHAR(length=32)),
)

class Measure(DeclarativeBase):
    __table__ = measures

    #relation definitions
    event_time = relation('EventTime', primaryjoin='Measure.id_eti_fk==EventTime.id_eti')
    quality_index = relation('QualityIndex', primaryjoin='Measure.id_qi_fk==QualityIndex.id_qi')
    obs_prop = relation('ObservedProperty', primaryjoin='Measure.id_opr_fk==ObservedProperty.id_opr')
    

class EventTime(DeclarativeBase):
    __tablename__ = 'event_time'

    __table_args__ = {}

    #column definitions
    id_eti = Column(u'id_eti', BIGINT(), primary_key=True, nullable=False)
    id_prc_fk = Column(u'id_prc_fk', INTEGER(), ForeignKey('procedures.id_prc'), nullable=False)
    time_eti = Column(u'time_eti', TIMESTAMP(timezone=True), nullable=False)

    #relation definitions
    measures = relation('Measure')
    procedures = relation('Procedure', primaryjoin='EventTime.id_prc_fk==Procedure.id_prc')
    quality_indexes = relation('QualityIndex', primaryjoin='EventTime.id_eti==Position.id_eti_fk', secondary=positions, secondaryjoin='Position.id_qi_fk==QualityIndex.id_qi')


class FeatureType(DeclarativeBase):
    __tablename__ = 'feature_type'

    __table_args__ = {}

    #column definitions
    id_fty = Column(u'id_fty', INTEGER(), primary_key=True, nullable=False)
    name_fty = Column(u'name_fty', VARCHAR(length=25), nullable=False)

    #relation definitions


class Foi(DeclarativeBase):
    __tablename__ = 'foi'

    __table_args__ = {}

    #column definitions
    desc_foi = Column(u'desc_foi', TEXT())
    #geom_foi = Column(u'geom_foi', NullType())
    geom_foi = GeometryColumn(u'geom_foi',Geometry(dimension=3,srid=21781), comparator=PGComparator)
    id_foi = Column(u'id_foi', INTEGER(), primary_key=True, nullable=False)
    id_fty_fk = Column(u'id_fty_fk', INTEGER(), ForeignKey('feature_type.id_fty'), nullable=False)
    name_foi = Column(u'name_foi', VARCHAR(length=25))

    #relation definitions
    feature_type = relation('FeatureType', primaryjoin='Foi.id_fty_fk==FeatureType.id_fty')
    time_res_units = relation('TimeResUnit', primaryjoin='Foi.id_foi==Procedure.id_foi_fk', secondary=procedures, secondaryjoin='Procedure.id_tru_fk==TimeResUnit.id_tru')

GeometryDDL(Foi.__table__)


class Measure(DeclarativeBase):
    __table__ = measures


    #relation definitions
    event_time = relation('EventTime', primaryjoin='Measure.id_eti_fk==EventTime.id_eti')
    quality_index = relation('QualityIndex', primaryjoin='Measure.id_qi_fk==QualityIndex.id_qi')


class ObsType(DeclarativeBase):
    __tablename__ = 'obs_type'

    __table_args__ = {}

    #column definitions
    desc_oty = Column(u'desc_oty', VARCHAR(length=120))
    id_oty = Column(u'id_oty', INTEGER(), primary_key=True, nullable=False)
    name_oty = Column(u'name_oty', VARCHAR(length=60), nullable=False)

    #relation definitions
    time_res_units = relation('TimeResUnit', primaryjoin='ObsType.id_oty==Procedure.id_oty_fk', secondary=procedures, secondaryjoin='Procedure.id_tru_fk==TimeResUnit.id_tru')


class ObservedProperty(DeclarativeBase):
    __tablename__ = 'observed_properties'

    __table_args__ = {}

    #column definitions
    desc_opr = Column(u'desc_opr', TEXT())
    id_opr = Column(u'id_opr', INTEGER(), primary_key=True, nullable=False)
    name_opr = Column(u'name_opr', VARCHAR(length=60), nullable=False)

    #relation definitions
    procedures = relation('Procedure', primaryjoin='ObservedProperty.id_opr==ProcOb.id_opr_fk', secondary=proc_obs, secondaryjoin='ProcOb.id_prc_fk==Procedure.id_prc')


class OffProc(DeclarativeBase):
    __table__ = off_proc


    #relation definitions
    procedures = relation('Procedure', primaryjoin='OffProc.id_prc_fk==Procedure.id_prc')
    offerings = relation('Offering', primaryjoin='OffProc.id_off_fk==Offering.id_off')


class Offering(DeclarativeBase):
    __tablename__ = 'offerings'

    __table_args__ = {}

    #column definitions
    active_off = Column(u'active_off', BOOLEAN(), nullable=False)
    desc_off = Column(u'desc_off', TEXT())
    expiration_off = Column(u'expiration_off', TIMESTAMP(timezone=True))
    id_off = Column(u'id_off', INTEGER(), primary_key=True, nullable=False)
    name_off = Column(u'name_off', VARCHAR(length=10), nullable=False)

    #relation definitions
    procedures = relation('Procedure', primaryjoin='Offering.id_off==OffProc.id_off_fk', secondary=off_proc, secondaryjoin='OffProc.id_prc_fk==Procedure.id_prc')


class Position(DeclarativeBase):
    __table__ = positions
    
    #column definitions
    #geom_pos = GeometryColumn(u'geom_pos',Point(dimension=3,srid=21781),nullable=False, comparator=PGComparator)

    #relation definitions
    event_time = relation('EventTime', primaryjoin='Position.id_eti_fk==EventTime.id_eti')
    quality_index = relation('QualityIndex', primaryjoin='Position.id_qi_fk==QualityIndex.id_qi')

"""
class Position(DeclarativeBase):
    __table__ = positions
    extend_existing=True
    __table_args__ = {}
    
    #column definitions
    id_pos = Column(u'id_pos', BIGINT(), primary_key=True, nullable=False)
    id_qi_fk = Column(u'id_qi_fk', INTEGER(), ForeignKey('quality_index.id_qi'), nullable=False)
    id_eti_fk = Column(u'id_eti_fk', BIGINT(), ForeignKey('event_time.id_eti'), nullable=False)
    geom_pos = GeometryColumn(u'geom_pos',Point(2,21781),nullable=False, comparator=PGComparator)
    #Column(u'geom_pos', NullType(), nullable=False),
    
    #relation definitions
    event_time = relation('EventTime', primaryjoin='Position.id_eti_fk==EventTime.id_eti')
    quality_index = relation('QualityIndex', primaryjoin='Position.id_qi_fk==QualityIndex.id_qi')

GeometryDDL(Position.__table__)
"""

class ProcOb(DeclarativeBase):
    __table__ = proc_obs


    #relation definitions
    uoms = relation('Uom', primaryjoin='ProcOb.id_uom_fk==Uom.id_uom')
    procedures = relation('Procedure', primaryjoin='ProcOb.id_prc_fk==Procedure.id_prc')
    observed_properties = relation('ObservedProperty', primaryjoin='ProcOb.id_opr_fk==ObservedProperty.id_opr')


class Procedure(DeclarativeBase):
    __table__ = procedures


    #relation definitions
    time_res_unit = relation('TimeResUnit', primaryjoin='Procedure.id_tru_fk==TimeResUnit.id_tru')
    obs_type = relation('ObsType', primaryjoin='Procedure.id_oty_fk==ObsType.id_oty')
    foi = relation('Foi', primaryjoin='Procedure.id_foi_fk==Foi.id_foi')
    offerings = relation('Offering', primaryjoin='Procedure.id_prc==OffProc.id_prc_fk', secondary=off_proc, secondaryjoin='OffProc.id_off_fk==Offering.id_off')
    uoms = relation('Uom', primaryjoin='Procedure.id_prc==ProcOb.id_prc_fk', secondary=proc_obs, secondaryjoin='ProcOb.id_uom_fk==Uom.id_uom')


class QualityIndex(DeclarativeBase):
    __tablename__ = 'quality_index'

    __table_args__ = {}

    #column definitions
    desc_qi = Column(u'desc_qi', TEXT())
    id_qi = Column(u'id_qi', INTEGER(), primary_key=True, nullable=False)
    name_qi = Column(u'name_qi', VARCHAR(length=25), nullable=False)

    #relation definitions
    event_times = relation('EventTime', primaryjoin='QualityIndex.id_qi==Position.id_qi_fk', secondary=positions, secondaryjoin='Position.id_eti_fk==EventTime.id_eti')


class TimeResUnit(DeclarativeBase):
    __tablename__ = 'time_res_unit'

    __table_args__ = {}

    #column definitions
    id_tru = Column(u'id_tru', INTEGER(), primary_key=True, nullable=False)
    name_tru = Column(u'name_tru', VARCHAR(length=15))

    #relation definitions
    obs_types = relation('ObsType', primaryjoin='TimeResUnit.id_tru==Procedure.id_tru_fk', secondary=procedures, secondaryjoin='Procedure.id_oty_fk==ObsType.id_oty')


class Uom(DeclarativeBase):
    __tablename__ = 'uoms'

    __table_args__ = {}

    #column definitions
    desc_uom = Column(u'desc_uom', TEXT())
    id_uom = Column(u'id_uom', INTEGER(), primary_key=True, nullable=False)
    name_uom = Column(u'name_uom', VARCHAR(length=20), nullable=False)

    #relation definitions
    procedures = relation('Procedure', primaryjoin='Uom.id_uom==ProcOb.id_uom_fk', secondary=proc_obs, secondaryjoin='ProcOb.id_prc_fk==Procedure.id_prc')


