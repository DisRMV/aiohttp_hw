from aiohttp import web
from models import db, User
from models import Advertisements as Ads
from config import POSTGRES_URI
from validators import validate_user_post, validate_adv_post


app = web.Application()


async def init_app(app):
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()


class AdvertisementsView(web.View):

    async def get(self):
        query_set = await Ads.query.gino.all()
        data = [ads.to_dict() for ads in query_set]
        return web.json_response(data)

    async def get_by_id(self):
        advs_id = int(self.match_info['advs_id'])
        query_set = await Ads.get(advs_id)
        return web.json_response(query_set.to_dict())

    async def post(self):
        data = await self.request.json()
        data = validate_adv_post(data)
        advs = await Ads.create(title=data['title'], description=data.get('description'), owner_id=data['owner_id'])
        return web.json_response(advs.to_dict())

    async def delete(self):
        advs_id = int(self.request.match_info['advs_id'])
        adv = await Ads.get(advs_id)
        response = adv.to_dict()
        response['message'] = 'Advertisement successfully deleted'
        await adv.delete()
        return web.json_response(response)


class UserView(web.View):

    async def post(self):
        data = await self.request.json()
        data = validate_user_post(data)
        user = await User.create(name=data.get('name'), email=data.get('email'), password=data.get('password'))
        return web.json_response(user.to_dict())


app.cleanup_ctx.append(init_app)
app.add_routes([web.get('/advs', AdvertisementsView.get),
                web.get(r'/advs/{advs_id:\d+}', AdvertisementsView.get_by_id),
                web.post('/advs', AdvertisementsView),
                web.delete(r'/advs/{advs_id:\d+}', AdvertisementsView),
                web.post('/user', UserView)])
