from meijer_funcs import clip_meijer_coupon, init_meijer_connection_user, unclip_meijer_coupon, get_all_clipped_meijer_coupons, get_meijer_offers, strip_tags
import argparse
from tqdm import trange, tqdm
import json

parser = argparse.ArgumentParser(description="Finds  Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",								required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",																required=True,	type=str)
parser.add_argument("-r",	"--prefix",			help="prefix (6 digits)",												required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)

results = []
validids = []
tounclip = []
for offerid in trange(int(f'{args.prefix}0000'), int(f'{args.prefix}9999')+1):
	result = clip_meijer_coupon(offerid)
	if result == True:
		validids.append(offerid)
	else:
		results.append({'meijerOfferId': offerid, 'status': result})

for offertype in ['Earned', 'InProgress', 'Available']:
	offers = get_meijer_offers(offertype)
	if offers:
		for offer in sorted(offers, key = lambda i: i['meijerOfferId']):
			if offer.get("meijerOfferId") in validids:
				print(f'{offer.get("meijerOfferId")} - {offertype} reward - {offer.get("title").strip()} {strip_tags(offer.get("description")).strip()}')
				results.append({'meijerOfferId': offer.get("meijerOfferId"), 'status': f'{offertype} reward', 'description': f'{offer.get("title").strip()} {strip_tags(offer.get("description")).strip()}', 'expirationDate': offer.get("expirationDate")})

coupons = get_all_clipped_meijer_coupons()
if coupons:
	for coupon in sorted(coupons, key = lambda i: i['meijerOfferId']):
		if coupon.get("meijerOfferId") in validids:
			print(f'{coupon.get("meijerOfferId")} - coupon - {coupon.get("title").strip()} {coupon.get("description").strip()}')
			results.append({'meijerOfferId': coupon.get("meijerOfferId"), 'status': 'Valid coupon', 'description': f'{coupon.get("title").strip()} {coupon.get("description").strip()}', 'expirationDate': coupon.get("redemptionEndDate")})
			tounclip.append(coupon.get("meijerOfferId"))

with open(f'{args.username}_{args.prefix}.txt', 'w') as outfile:
	json.dump(sorted(results, key = lambda i: i['meijerOfferId']), outfile, indent=2)

print('Unclipping please wait')
for offerid in tqdm(tounclip):
	unclip_meijer_coupon(offerid)