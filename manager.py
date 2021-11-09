from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import delete, select, update, desc
from sqlalchemy.sql.functions import func

from models import Team as TeamModel, Member as MemberModel
from schemas import Member as MemberSchema
from utils.exceptions import NotFoundException


class TeamDAL:

    @staticmethod
    async def get_average_age(session: Session, order_by_desc: int):
        average_field_label = 'average'
        stmt = select(TeamModel.id, TeamModel.name, func.avg(MemberModel.age).label(average_field_label)).join(TeamModel, TeamModel.id==MemberModel.team_id).group_by(TeamModel.id)
        if order_by_desc:
            stmt = stmt.order_by(desc(average_field_label))
        else:
            stmt = stmt.order_by(average_field_label)
        q = await session.execute(stmt)
        return q.fetchall()


class MemberDal:

    @staticmethod
    async def get_by_id(session: AsyncSession, member_id: int):
        q = await session.execute(select(MemberModel).where(MemberModel.id==member_id))
        player = q.scalars().first()
        print(player, 'aaa')
        if not player:
            raise NotFoundException()
        return player

    @staticmethod
    async def create(session: AsyncSession, member: MemberSchema):
        player = MemberModel(team_id=member.team_id, age=member.age, name=member.name)
        session.add(player)
        await session.flush()
        # await session.refresh(player)
        return player

    @staticmethod
    async def update(session: Session, member_id: int, member: MemberSchema):
        await MemberDal.get_by_id(session, member_id)
        values = member.dict()
        del(values['id'])
        stmt = update(MemberModel).where(MemberModel.id==member_id).values(**values)
        await session.execute(stmt)
        session.flush()
        return await MemberDal.get_by_id(session, member_id)

    @staticmethod
    async def delete(session: Session, member_id: int):
        await MemberDal.get_by_id(session, member_id)
        stmt = delete(MemberModel).where(MemberModel.id==member_id)
        await session.execute(stmt)
        return True
