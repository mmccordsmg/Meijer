from meijer_funcs import init_meijer_connection_guest, create_meijer_account, clip_meijer_coupon, init_meijer_connection_user
import argparse


parser = argparse.ArgumentParser(description="Creates Mejier account using information provided in arguments")
parser.add_argument("-n",	"--phone",			help="Phone#",											required=True,	type=str)
parser.add_argument("-p",	"--password",		help="Password",										required=True,	type=str)
parser.add_argument("-f",	"--firstname",	help="First Name",									required=True,	type=str)
parser.add_argument("-l",	"--lastname",		help="Last Name",										required=True,	type=str)
parser.add_argument("-e",	"--email",			help="Email address",								required=True,	type=str)
parser.add_argument("-z",	"--zipcode",		help="Zip Code",										required=False,	type=str, default='49341')
parser.add_argument("-s",	"--storeId",		help="Default store Id",						required=False,	type=int, default=226)
parser.add_argument("-i",	"--pin",				help="account PIN",									required=True,	type=str)
parser.add_argument("-c",	"--clipfile",		help="file with offerids to clip", 	required=True,	type=str)


args = parser.parse_args()

init_meijer_connection_guest()
account = create_meijer_account (args.phone, args.password, args.firstname, args.lastname, args.email, args.zipcode, args.storeId, args.pin)
if account:
	print("Account %s created successfully for %s (%s)." % (account, args.email, args.phone))
	
init_meijer_connection_user(args.email, args.password)

f = open(f'{args.clipfile}', 'r')

for line in f:
	offerid = line.split()[0]
	if (result := clip_meijer_coupon(offerid)) == True:
		print(f"Clipped offer {offerid} successfully on account {args.email}.")
	else:
		print (f"Error clipping coupon {offerid} - {result}")