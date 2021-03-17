from meijer_funcs import clip_meijer_coupon, init_meijer_connection_user
import argparse

parser = argparse.ArgumentParser(description="Clips specified Meijer coupons for account specified")
parser.add_argument("-u",	"--username",		help="Username (Email address)",		required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-f",	"--filename",		help="file with offerids",				required=True,	type=str)

args = parser.parse_args()

init_meijer_connection_user(args.username, args.password)

f = open(f'{args.filename}', 'r')

for line in f:
	offerid = line.split()[0]
	result = clip_meijer_coupon(offerid)
	if not result == True:
		print (f"Error clipping coupon {offerid} - {result}")
		exit()
	else:
		print(f"Clipped offer {offerid} successfully on account {args.username}.")