# Proxy6
-------

Proxy6 is an easy-to-use fully asynchronous API Wrapper for [Proxy6](https://proxy6.net/en/?r=516277) service. With Proxy6, you can easily retrieve lists of purchased proxies, buy new ones, prolong previously purchased and etc.

## Usage
To use Proxy6, you'll need to sign up for an account on the [Proxy6](https://proxy6.net/en/?r=516277) website and [obtain an API key](https://proxy6.net/en/user/developers). 
Once you have an API key, you can create a ProxySix object and use its methods.

Here's an example of how to use Proxy6 to retrieve a list of proxies and filter them by country:

```
import asyncio
from proxy6 import ProxySix

# Replace YOUR_API_KEY with your actual API key
client = ProxySix(api_key='API_KEY_HERE')

# Retrieve a list of purchased proxies and print their IPs
async def main():
    my_proxies = await client.getProxy(nokey=True)
    for proxy in my_proxies.list:
        check = await client.checkProxy(proxy.id)
        if check:
            status = "- this proxy works!"
        else:
            status = "- this proxy does not work :("
        print(proxy.ip, status)
        
if __name__ == "__main__":
    asyncio.run(main())
```

All the methods are well documented. Package supports type hinting so you can play around this module and explore features on your own.

# Contributing
Contributions to Proxy6 are welcome and appreciated! If you'd like to contribute, please fork the repository and submit a pull request with your changes.

# License
Proxy6 is licensed under the MIT License. See the LICENSE file for more information.

# Contact
If you have any questions or comments about Proxy6, feel free to contact the author at nidobrydnev@gmail.com