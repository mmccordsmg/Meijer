from meijer_funcs import clip_meijer_coupon, init_meijer_connection_user, unclip_meijer_coupon, get_all_clipped_meijer_coupons, get_meijer_offers, strip_tags
import argparse
from tqdm import trange, tqdm
import json
import random
from datetime import datetime

parser = argparse.ArgumentParser(description="Finds  Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",								required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",																required=True,	type=str)
#parser.add_argument("-r",	"--prefix",			help="prefix (6 digits)",												required=True,	type=str)
parser.add_argument("-s",	"--startnum",		help="starting number (10 digits)",							required=True,	type=str)
parser.add_argument("-e",	"--endnum",			help="ending number (10 digits)",								required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)
if len(args.startnum) != 10:
	print('Wrong startnum length')
	exit()
if len(args.endnum) != 10:
	print('Wrong endnum length')
	exit()
if int(args.startnum) > int(args.endnum):
	print('startnum must be less than endnum')
	exit()
	
results = []

checkrange = []

outname = f'{args.username}_{args.startnum}-{args.endnum}_{datetime.now().strftime("%Y-%m-%d-%H_%M_%S")}.txt'

for x in range(int(args.startnum), int(args.endnum)+1):
	checkrange.append(x)

def process_coupons():
	global results, checkrange
	coupons = get_all_clipped_meijer_coupons()
	if coupons:
		for coupon in sorted(coupons, key = lambda i: i['meijerOfferId']):
			if coupon.get("meijerOfferId") in checkrange:
				#print(f'{coupon.get("meijerOfferId")} - coupon - {coupon.get("title").strip()} {coupon.get("description").strip()}')
				results.append({'meijerOfferId': coupon.get("meijerOfferId"), 'status': 'Valid coupon', 'description': f'{coupon.get("title").strip()} {coupon.get("description").strip()}', 'expirationDate': coupon.get("redemptionEndDate")})
				unclip_meijer_coupon(coupon.get("meijerOfferId"))
		
for offerid in tqdm(checkrange):
	if offerid%500 == 0:
		process_coupons()
	result = clip_meijer_coupon(offerid)
	#if result == 'Success':
		#print(f'{offerid}: Success!')
	if (not result == True) and (not result == 'Offer is already clipped by this shopper.'):
		results.append({'meijerOfferId': offerid, 'status': result})

for offertype in ['Earned', 'InProgress', 'Available']:
	offers = get_meijer_offers(offertype)
	if offers:
		for offer in sorted(offers, key = lambda i: i['meijerOfferId']):
			if offer.get("meijerOfferId") in checkrange:
				#print(f'{offer.get("meijerOfferId")} - {offertype} reward - {offer.get("title").strip()} {strip_tags(offer.get("description")).strip()}')
				results.append({'meijerOfferId': offer.get("meijerOfferId"), 'status': f'{offertype} reward', 'description': f'{offer.get("title").strip()} {strip_tags(offer.get("description")).strip()}', 'expirationDate': offer.get("expirationDate")})

process_coupons()

with open(outname, 'w') as outfile:
	json.dump(sorted(results, key = lambda i: i['status']), outfile, indent=2)
