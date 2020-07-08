import json
import random
import aiohttp
import asyncio

url = 'http://localhost:8080'
iterations = 1000000


def generate_random_string(strlength):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    s = ""
    for _ in range(strlength):
        idx = random.randint(0, 61)
        s += chars[idx]
    return s


async def main():
    async with aiohttp.ClientSession() as session:
        teststore = []
        for it in range(iterations):
            # generate random value string
            v1 = random.randint(100, 500)
            value = generate_random_string(v1)
            payload = {'action': 'insert', 'key': str(it), 'val': str(value)}
            async with session.post(url, json=payload) as resp:
                status = resp.status
                if status != 200:
                    print("Unsuccessful insert from HTTP - code={} with payload:\n{} ".format(status, payload))
                    continue
                msg = await resp.text()
                answer = json.loads(msg)
                # print("Response {} received: {}".format(resp.status, msg))
                # print("action: {}, key: {}, value: {}, success: {}".format(jmsg['action'], jmsg['key'], jmsg['val'], jmsg['success']))
                if not answer['success']:
                    print("Unsuccessful insert at Database: ", answer)
                    continue

                teststore.append(value)
                if it % 10000 == 0:
                    print("---> Insert Iteration: ", it)

        for it in range(iterations):
            payload = {'action': 'find', 'key': str(it), 'val': ''}
            async with session.post(url, json=payload) as resp:
                status = resp.status
                if status != 200:
                    print("Unsuccessful retrieve from HTTP - code={} with payload:\n{} ".format(status, payload))
                    continue
                msg = await resp.text()
                answer = json.loads(msg)

                if not answer['success']:
                    print("Unsuccessful retrieve from Database: ", answer)
                    continue

                if answer['val'] != teststore[it]:
                    print("Retrieve does not match teststore: ", answer)
                    continue

            if it % 10000 == 0:
                print("---> Retrieve Iteration: ", it)


if __name__ == "__main__":
    # main()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())