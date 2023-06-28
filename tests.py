import unittest
from unittest import IsolatedAsyncioTestCase
import os

from proxy6 import ProxySix
from proxy6 import ProxyCountry, ProxyScheme, ProxyVersion, ProxyState
from proxy6.exceptions import (
    InvalidAPIKey,
    InvalidCount
)


API_KEY = os.environ.get("API_KEY", None)

class TestProxySix(IsolatedAsyncioTestCase):
    def setUp(self):
        self.proxy_provider = ProxySix(api_key=API_KEY)

    async def test_invalidAPIkey(self):
        self.invalid_provider = ProxySix('-')
        with self.assertRaises(InvalidAPIKey):
            await self.invalid_provider.getCountry()

    async def test_getPrice(self):
        res = await self.proxy_provider.getPrice(1, 1, ProxyVersion.IPv6)
        self.assertIsInstance(res.price_single, float)
        self.assertIsInstance(res.price, float)
        self.assertEqual(res.period, 1, "Given period is not equal to one that's been received")
        self.assertEqual(res.count, 1, "Given count is not equal to one that have's been received")

        with self.assertRaises(InvalidCount):
            await self.proxy_provider.getPrice(0, 3)

    async def test_getCount(self):
        res = await self.proxy_provider.getCount(ProxyCountry.GERMANY, ProxyVersion.IPv6)
        self.assertIsInstance(res, int)

    async def test_getCountry(self):
        for ver in [ProxyVersion.IPv4, ProxyVersion.IPv4Shared, ProxyVersion.IPv6]:
            res = await self.proxy_provider.getCountry(version=ver)
            self.assertIsInstance(res, list)
            for country in res:
                self.assertIsInstance(country, ProxyCountry)

    async def test_getProxy(self):
        res_key = await self.proxy_provider.getProxy(nokey=False)
        self.assertIsInstance(res_key.list, dict)
        self.assertEqual(res_key.list_count, len(res_key.list.keys()))
        for key, value in res_key.list.items():
            self.assertEqual(key, value.id)
        res_nokey = await self.proxy_provider.getProxy(nokey=True)
        self.assertIsInstance(res_nokey.list, list)
        self.assertEqual(res_nokey.list_count, len(res_nokey.list))

        res_limit = await self.proxy_provider.getProxy(nokey=True, limit=1)
        self.assertTrue(res_limit.list_count <= 1)

        res_active = await self.proxy_provider.getProxy(state=ProxyState.ACTIVE)
        res_expired = await self.proxy_provider.getProxy(state=ProxyState.EXPIRED)
        res_all = await self.proxy_provider.getProxy(state=ProxyState.all)
        self.assertNotEqual(res_active.list_count, res_expired.list_count)
        self.assertEqual(res_active.list_count + res_expired.list_count, res_all.list_count)


    async def test_setType(self):
        proxies = await self.proxy_provider.getProxy(nokey=True)
        if proxies.list_count > 0:
            proxy = proxies.list[0]
            if proxy.type == ProxyScheme.HTTPS:
                new_type = ProxyScheme.SOCKS5
            else:
                new_type = ProxyScheme.HTTPS
            res_new = await self.proxy_provider.setType(ids=[proxy.id], type=new_type)
            self.assertTrue(res_new)
            res_old = await self.proxy_provider.setType(ids=[proxy.id], type=proxy.type)
            self.assertTrue(res_old)

    async def test_setDescription(self):
        proxies = await self.proxy_provider.getProxy(nokey=True)
        if proxies.list_count > 0:
            proxy = proxies.list[0]
            descr_old = proxy.descr
        descr_new = descr_old + f" {proxy.id}"
        new = await self.proxy_provider.setDescription(descr_new, ids=[proxy.id])
        self.assertEqual(new, 1)
        proxies = await self.proxy_provider.getProxy(description=descr_old + f" {proxy.id}", nokey=True)
        self.assertEqual(proxies.list_count, 1)

    async def test_buyProxy(self):
        '''
        Test proxy purchasing.

        **Please, be aware that you can lose funcs while running this test**
        '''
        buy_proxy = await self.proxy_provider.buyProxy(1, 1, ProxyCountry.GERMANY, description="proxy#1111", nokey=True)
        proxy = buy_proxy.list[0]
        self.assertEqual(buy_proxy.count, 1)
        self.assertEqual(buy_proxy.period, 1)
        self.assertEqual(len(buy_proxy.list), buy_proxy.count)
        self.assertEqual(buy_proxy.country, ProxyCountry.GERMANY)
        self.assertEqual(proxy.proxy_link, f"http://{proxy.user}:{proxy.pswd}@{proxy.host}:{proxy.port}")

    async def test_prolongProxy(self):
        proxies = await self.proxy_provider.getProxy(nokey=True)
        if proxies.list_count > 1:
            proxy1 = proxies.list[0]
            proxy2 = proxies.list[1]
            prolong_list = await self.proxy_provider.prolongProxy(3, [proxy1.id, proxy2.id])
            self.assertEqual(prolong_list.period, 3)
            self.assertEqual(prolong_list.count, len(prolong_list.list.values()))
            self.assertTrue((prolong_list.list[proxy1.id].unixtime_end - proxy1.unixtime)/86400 > 3)
            self.assertTrue((prolong_list.list[proxy2.id].unixtime_end - proxy2.unixtime)/86400 > 3)
        elif proxies.list_count > 0:
            proxy = proxies.list[0]
            prolong_list = await self.proxy_provider.prolongProxy(3, [proxy.id])
            self.assertEqual(prolong_list.period, 3)
            self.assertEqual(prolong_list.count, len(prolong_list.list.values()))
            self.assertTrue((prolong_list.list[proxy.id].unixtime_end - proxy.unixtime)/86400 > 3)

    async def test_deleteProxy(self):
        proxies = await self.proxy_provider.getProxy(nokey=True)
        if proxies.list_count > 0:
            proxy_to_delete = proxies.list[-1]
            delete = await self.proxy_provider.deleteProxy(ids=[proxy_to_delete.id])
            self.assertEqual(delete, 1)
            proxies_new = await self.proxy_provider.getProxy(nokey=True)
            ids = [proxy.id for proxy in proxies_new.list]
            self.assertNotIn(proxy_to_delete.id, ids)
            self.assertEqual(proxies.list_count - 1, proxies_new.list_count)



    async def test_checkProxy(self):
        proxy_active = await self.proxy_provider.getProxy(ProxyState.ACTIVE, nokey=True)
        if proxy_active.list_count > 0:
            proxy = proxy_active.list[0]
            proxy_check = await self.proxy_provider.checkProxy(proxy.id)
            self.assertTrue(proxy_check)
        proxy_inactive = await self.proxy_provider.getProxy(ProxyState.EXPIRED, nokey=True)
        if proxy_inactive.list_count > 0:
            proxy = proxy_inactive.list[0]
            proxy_check = await self.proxy_provider.checkProxy(proxy.id)
            self.assertFalse(proxy_check)


if __name__ == '__main__':
    unittest.main()