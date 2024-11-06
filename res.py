import requests
import json

def get_res(hotel_id, token):

    url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/rsv/v1/hotels/{hotel_id}/reservations?limit=50&departureEndDate=2024-10-12&departureStartDate=2024-10-10&reservationStatuses=CheckedOut"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel_id,
    'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    

    content = response.json()

    res = [x['reservationIdList'][0]['id'] for x in content['reservations']['reservationInfo']]
    print("Reservas:", res)
    return res

def get_res_by_confirmation(confirmation, hotel_id, token):

    url = f"https://acc2-oc.hospitality-api.us-ashburn-1.ocs.oraclecloud.com/rsv/v1/hotels/{hotel_id}/reservations?confirmationNumberList={confirmation}"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel_id,
    'x-app-key': '5502014f-a4f1-4135-9d45-ae5fd594eba5',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.ok:
        try:
            return response.json()['reservations']['reservationInfo'][0]['reservationIdList'][0]['id']
        except:
            return None
        
    else:
        return None
