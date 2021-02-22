from meijer_funcs import unclip_meijer_coupon, get_all_clipped_meijer_coupons, init_meijer_connection_user, get_meijer_offers
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Unclips all clipped Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)

coupons = get_all_clipped_meijer_coupons()
	
if coupons:
	for coupon in tqdm(coupons):
		result = unclip_meijer_coupon(coupon["meijerOfferId"])
		if not result:
			print (f'Error unclipping coupon {coupon["meijerOfferId"]} - {coupon["title"].strip()} {coupon["description"].strip()}')
else:
	print ("No clipped coupons found.")
