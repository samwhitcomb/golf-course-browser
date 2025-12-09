#!/usr/bin/env python3
"""
Generate 250 igolf courses (radar mapped, +/-5m accuracy) that appear only in search results.
These courses are excluded from carousels and map view.
"""

import json
import re
from pathlib import Path

COURSES_FILE = Path('courses.json')

# Course data with realistic names, locations, and brief descriptions
IGOLF_COURSES = [
    # UK - England (30 courses)
    {"name": "Brampton Park Golf Club", "location": "Brampton, England", "continent": "Europe", "type": "parkland", "lat": 52.3209, "lng": -0.2206, "desc": "A pleasant parkland course set in the Cambridgeshire countryside, offering a friendly and accessible round for golfers of all abilities."},
    {"name": "Braintree Golf Club", "location": "Braintree, England", "continent": "Europe", "type": "parkland", "lat": 51.8780, "lng": 0.5506, "desc": "A traditional English parkland course with mature trees and well-maintained fairways, providing a classic golfing experience."},
    {"name": "Bromley Golf Club", "location": "Bromley, England", "continent": "Europe", "type": "parkland", "lat": 51.4050, "lng": 0.0158, "desc": "A well-established parkland course in suburban London, featuring tree-lined fairways and challenging greens."},
    {"name": "Burnham Beeches Golf Club", "location": "Burnham, England", "continent": "Europe", "type": "parkland", "lat": 51.5400, "lng": -0.6580, "desc": "A scenic parkland course set within ancient woodland, offering a peaceful and natural golfing environment."},
    {"name": "Canterbury Golf Club", "location": "Canterbury, England", "continent": "Europe", "type": "parkland", "lat": 51.2790, "lng": 1.0790, "desc": "A historic parkland course near the famous cathedral city, combining tradition with modern course maintenance."},
    {"name": "Cheshunt Park Golf Club", "location": "Cheshunt, England", "continent": "Europe", "type": "parkland", "lat": 51.7000, "lng": -0.0300, "desc": "A welcoming parkland course in Hertfordshire, ideal for both casual and competitive play."},
    {"name": "Chigwell Golf Club", "location": "Chigwell, England", "continent": "Europe", "type": "parkland", "lat": 51.6180, "lng": 0.0750, "desc": "A well-maintained parkland course in Essex, featuring strategic bunkering and varied hole designs."},
    {"name": "Cobtree Manor Golf Club", "location": "Maidstone, England", "continent": "Europe", "type": "parkland", "lat": 51.2700, "lng": 0.5200, "desc": "A modern parkland course set in the Kent countryside, offering excellent facilities and enjoyable golf."},
    {"name": "Colchester Golf Club", "location": "Colchester, England", "continent": "Europe", "type": "parkland", "lat": 51.8950, "lng": 0.9040, "desc": "One of England's oldest golf clubs, featuring a traditional parkland layout with historic character."},
    {"name": "Coombe Hill Golf Club", "location": "Kingston upon Thames, England", "continent": "Europe", "type": "parkland", "lat": 51.4130, "lng": -0.3000, "desc": "A challenging parkland course in Surrey, known for its undulating terrain and strategic design."},
    {"name": "Cranfield Golf Club", "location": "Cranfield, England", "continent": "Europe", "type": "parkland", "lat": 52.0730, "lng": -0.6010, "desc": "A friendly parkland course in Bedfordshire, offering a relaxed atmosphere and good value golf."},
    {"name": "Dartford Golf Club", "location": "Dartford, England", "continent": "Europe", "type": "parkland", "lat": 51.4470, "lng": 0.2200, "desc": "A traditional parkland course in Kent, featuring mature trees and well-established greens."},
    {"name": "Dunstable Downs Golf Club", "location": "Dunstable, England", "continent": "Europe", "type": "parkland", "lat": 51.8600, "lng": -0.5200, "desc": "A scenic parkland course on the Chiltern Hills, offering panoramic views and challenging play."},
    {"name": "Ealing Golf Club", "location": "Ealing, England", "continent": "Europe", "type": "parkland", "lat": 51.5120, "lng": -0.3080, "desc": "A well-established parkland course in West London, providing accessible golf in an urban setting."},
    {"name": "Earlswood Lakes Golf Club", "location": "Earlswood, England", "continent": "Europe", "type": "parkland", "lat": 52.3700, "lng": -1.8500, "desc": "A scenic parkland course set around beautiful lakes, offering a peaceful and enjoyable round."},
    {"name": "East Herts Golf Club", "location": "Hertford, England", "continent": "Europe", "type": "parkland", "lat": 51.7950, "lng": -0.0780, "desc": "A traditional parkland course in Hertfordshire, featuring classic English golf course design."},
    {"name": "Epping Golf Club", "location": "Epping, England", "continent": "Europe", "type": "parkland", "lat": 51.7000, "lng": 0.1100, "desc": "A well-maintained parkland course in Essex, offering good value and enjoyable golf."},
    {"name": "Faversham Golf Club", "location": "Faversham, England", "continent": "Europe", "type": "parkland", "lat": 51.3150, "lng": 0.8920, "desc": "A friendly parkland course in Kent, known for its welcoming atmosphere and reasonable green fees."},
    {"name": "Felixstowe Ferry Golf Club", "location": "Felixstowe, England", "continent": "Europe", "type": "links", "lat": 51.9600, "lng": 1.3600, "desc": "A traditional links course on the Suffolk coast, offering authentic seaside golf with coastal winds."},
    {"name": "Frinton Golf Club", "location": "Frinton-on-Sea, England", "continent": "Europe", "type": "links", "lat": 51.8300, "lng": 1.2400, "desc": "A classic links course on the Essex coast, featuring firm fairways and challenging bunkers."},
    {"name": "Gog Magog Golf Club", "location": "Cambridge, England", "continent": "Europe", "type": "parkland", "lat": 52.2000, "lng": 0.1500, "desc": "A well-regarded parkland course near Cambridge, offering excellent conditioning and strategic design."},
    {"name": "Gosforth Park Golf Club", "location": "Newcastle upon Tyne, England", "continent": "Europe", "type": "parkland", "lat": 55.0080, "lng": -1.6170, "desc": "A parkland course in the North East, featuring mature trees and well-designed holes."},
    {"name": "Hainault Forest Golf Club", "location": "Hainault, England", "continent": "Europe", "type": "parkland", "lat": 51.6000, "lng": 0.1000, "desc": "A parkland course set within ancient forest, offering a natural and peaceful golfing experience."},
    {"name": "Hampstead Golf Club", "location": "Hampstead, England", "continent": "Europe", "type": "parkland", "lat": 51.5550, "lng": -0.1750, "desc": "A historic parkland course in North London, combining tradition with modern course management."},
    {"name": "Harpenden Golf Club", "location": "Harpenden, England", "continent": "Europe", "type": "parkland", "lat": 51.8180, "lng": -0.3570, "desc": "A well-established parkland course in Hertfordshire, known for its excellent greens and friendly atmosphere."},
    {"name": "Harrow Golf Club", "location": "Harrow, England", "continent": "Europe", "type": "parkland", "lat": 51.5800, "lng": -0.3300, "desc": "A traditional parkland course in North West London, offering accessible golf in a suburban setting."},
    {"name": "Hertfordshire Golf Club", "location": "Hertford, England", "continent": "Europe", "type": "parkland", "lat": 51.7950, "lng": -0.0780, "desc": "A parkland course in the heart of Hertfordshire, featuring rolling fairways and strategic bunkering."},
    {"name": "Hockley Golf Club", "location": "Hockley, England", "continent": "Europe", "type": "parkland", "lat": 51.6000, "lng": 0.6500, "desc": "A friendly parkland course in Essex, offering good value and enjoyable golf for all abilities."},
    {"name": "Horsham Golf Club", "location": "Horsham, England", "continent": "Europe", "type": "parkland", "lat": 51.0630, "lng": -0.3270, "desc": "A well-maintained parkland course in West Sussex, featuring mature trees and challenging greens."},
    {"name": "Ilford Golf Club", "location": "Ilford, England", "continent": "Europe", "type": "parkland", "lat": 51.5600, "lng": 0.0700, "desc": "A parkland course in East London, providing accessible golf in an urban environment."},
    
    # UK - Scotland (10 courses)
    {"name": "Aberdeen Golf Club", "location": "Aberdeen, Scotland", "continent": "Europe", "type": "links", "lat": 57.1497, "lng": -2.0943, "desc": "A traditional links course on Scotland's east coast, offering classic seaside golf with challenging winds."},
    {"name": "Ayr Belleisle Golf Club", "location": "Ayr, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.4620, "lng": -4.6290, "desc": "A public parkland course in Ayrshire, offering accessible links-style golf in a beautiful coastal setting."},
    {"name": "Bathgate Golf Club", "location": "Bathgate, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.9020, "lng": -3.6430, "desc": "A well-established parkland course in West Lothian, featuring rolling terrain and strategic design."},
    {"name": "Bishopbriggs Golf Club", "location": "Bishopbriggs, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.9040, "lng": -4.2250, "desc": "A friendly parkland course near Glasgow, offering good value and enjoyable golf."},
    {"name": "Bonnyton Golf Club", "location": "Eaglesham, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.7400, "lng": -4.2700, "desc": "A parkland course in East Renfrewshire, featuring mature trees and well-maintained fairways."},
    {"name": "Cathkin Braes Golf Club", "location": "Glasgow, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.8000, "lng": -4.2000, "desc": "A challenging parkland course on the outskirts of Glasgow, offering panoramic city views."},
    {"name": "Cawder Golf Club", "location": "Glasgow, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.9000, "lng": -4.1500, "desc": "A well-regarded parkland course near Glasgow, featuring excellent conditioning and strategic design."},
    {"name": "Dalmahoy Golf Club", "location": "Kirknewton, Scotland", "continent": "Europe", "type": "parkland", "lat": 55.8800, "lng": -3.4300, "desc": "A parkland course near Edinburgh, set in beautiful countryside with excellent facilities."},
    {"name": "Dunbar Golf Club", "location": "Dunbar, Scotland", "continent": "Europe", "type": "links", "lat": 56.0020, "lng": -2.5200, "desc": "A classic links course on Scotland's east coast, offering authentic seaside golf with coastal challenges."},
    {"name": "Dunfermline Golf Club", "location": "Dunfermline, Scotland", "continent": "Europe", "type": "parkland", "lat": 56.0710, "lng": -3.4620, "desc": "A traditional parkland course in Fife, featuring mature trees and well-established greens."},
    
    # UK - Wales (5 courses)
    {"name": "Abergele Golf Club", "location": "Abergele, Wales", "continent": "Europe", "type": "parkland", "lat": 53.2800, "lng": -3.5800, "desc": "A scenic parkland course in North Wales, offering views of the coast and surrounding countryside."},
    {"name": "Cardiff Golf Club", "location": "Cardiff, Wales", "continent": "Europe", "type": "parkland", "lat": 51.4810, "lng": -3.1790, "desc": "A well-established parkland course in the Welsh capital, featuring mature trees and strategic design."},
    {"name": "Conwy Golf Club", "location": "Conwy, Wales", "continent": "Europe", "type": "links", "lat": 53.2800, "lng": -3.8300, "desc": "A traditional links course on the North Wales coast, offering challenging seaside golf."},
    {"name": "Pyle & Kenfig Golf Club", "location": "Porthcawl, Wales", "continent": "Europe", "type": "links", "lat": 51.5000, "lng": -3.7000, "desc": "A classic links course in South Wales, featuring firm fairways and natural dunes."},
    {"name": "Wrexham Golf Club", "location": "Wrexham, Wales", "continent": "Europe", "type": "parkland", "lat": 53.0460, "lng": -3.0000, "desc": "A friendly parkland course in North Wales, offering good value and enjoyable golf."},
    
    # Singapore (15 courses)
    {"name": "Changi Golf Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3640, "lng": 103.9900, "desc": "A well-maintained parkland course in eastern Singapore, offering tropical golf with excellent facilities."},
    {"name": "Keppel Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.2900, "lng": 103.8000, "desc": "A historic golf club in Singapore, featuring mature trees and traditional parkland design."},
    {"name": "Marina Bay Golf Course", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.2900, "lng": 103.8700, "desc": "A modern parkland course in the heart of Singapore, offering city views and excellent conditioning."},
    {"name": "NSRCC Changi", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3640, "lng": 103.9900, "desc": "A public golf course in eastern Singapore, providing accessible golf with good facilities."},
    {"name": "Orchid Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.4200, "lng": 103.8400, "desc": "A parkland course in northern Singapore, featuring tropical landscaping and well-designed holes."},
    {"name": "Raffles Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3500, "lng": 103.7000, "desc": "A well-established golf club in Singapore, offering excellent facilities and enjoyable parkland golf."},
    {"name": "Seletar Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.4100, "lng": 103.8700, "desc": "A parkland course in northern Singapore, featuring mature trees and strategic water hazards."},
    {"name": "Sentosa Golf Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.2500, "lng": 103.8300, "desc": "A premium parkland course on Sentosa Island, offering tropical golf with excellent maintenance."},
    {"name": "Singapore Island Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3500, "lng": 103.7800, "desc": "A prestigious golf club in Singapore, featuring multiple courses and excellent facilities."},
    {"name": "Tanah Merah Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3200, "lng": 103.9500, "desc": "A well-regarded golf club in eastern Singapore, offering championship-quality parkland courses."},
    {"name": "Warren Golf & Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3800, "lng": 103.7500, "desc": "A parkland course in Singapore, featuring tropical landscaping and challenging water features."},
    {"name": "Jurong Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3300, "lng": 103.7000, "desc": "A golf club in western Singapore, offering parkland golf with good facilities."},
    {"name": "Laguna National Golf Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3100, "lng": 103.9200, "desc": "A modern golf club in Singapore, featuring well-designed parkland courses with excellent conditioning."},
    {"name": "Sembawang Country Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.4500, "lng": 103.8200, "desc": "A parkland course in northern Singapore, offering tropical golf in a peaceful setting."},
    {"name": "Bukit Timah Golf Club", "location": "Singapore", "continent": "Asia", "type": "parkland", "lat": 1.3400, "lng": 103.7800, "desc": "A historic golf club in Singapore, featuring mature trees and traditional parkland design."},
    
    # Malaysia (20 courses)
    {"name": "A'Famosa Golf Resort", "location": "Malacca, Malaysia", "continent": "Asia", "type": "resort", "lat": 2.2000, "lng": 102.2500, "desc": "A resort golf course in historic Malacca, offering tropical golf with excellent facilities."},
    {"name": "Ayer Keroh Country Club", "location": "Malacca, Malaysia", "continent": "Asia", "type": "parkland", "lat": 2.2700, "lng": 102.2900, "desc": "A parkland course in Malacca, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Bukit Jambul Golf Club", "location": "Penang, Malaysia", "continent": "Asia", "type": "parkland", "lat": 5.3500, "lng": 100.2800, "desc": "A scenic parkland course in Penang, offering hilltop views and challenging golf."},
    {"name": "Clearwater Sanctuary Golf Resort", "location": "Kuala Lumpur, Malaysia", "continent": "Asia", "type": "resort", "lat": 3.1500, "lng": 101.7000, "desc": "A resort golf course near Kuala Lumpur, featuring water features and tropical design."},
    {"name": "Damai Laut Golf & Country Club", "location": "Lumut, Malaysia", "continent": "Asia", "type": "resort", "lat": 4.2000, "lng": 100.6500, "desc": "A coastal resort golf course, offering seaside golf with excellent facilities."},
    {"name": "Danau Golf Club", "location": "Kuala Lumpur, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.1500, "lng": 101.7000, "desc": "A parkland course in Kuala Lumpur, featuring mature trees and strategic water hazards."},
    {"name": "Glenmarie Golf & Country Club", "location": "Shah Alam, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.0800, "lng": 101.5500, "desc": "A well-regarded golf club near Kuala Lumpur, offering championship-quality parkland courses."},
    {"name": "Horizon Hills Golf & Country Club", "location": "Johor Bahru, Malaysia", "continent": "Asia", "type": "parkland", "lat": 1.5000, "lng": 103.6500, "desc": "A modern golf club in Johor, featuring well-designed parkland courses with excellent facilities."},
    {"name": "Kota Permai Golf & Country Club", "location": "Shah Alam, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.0800, "lng": 101.5500, "desc": "A parkland course near Kuala Lumpur, offering tropical golf with strategic design."},
    {"name": "Kuala Lumpur Golf & Country Club", "location": "Kuala Lumpur, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.1500, "lng": 101.7000, "desc": "A prestigious golf club in Kuala Lumpur, featuring multiple courses and excellent facilities."},
    {"name": "Palm Garden Golf Club", "location": "Putrajaya, Malaysia", "continent": "Asia", "type": "parkland", "lat": 2.9300, "lng": 101.7000, "desc": "A parkland course in Putrajaya, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Pangkor Laut Golf Club", "location": "Pangkor Island, Malaysia", "continent": "Asia", "type": "resort", "lat": 4.2000, "lng": 100.5500, "desc": "A resort golf course on Pangkor Island, offering tropical island golf with stunning views."},
    {"name": "Permas Jaya Golf & Country Club", "location": "Johor Bahru, Malaysia", "continent": "Asia", "type": "parkland", "lat": 1.5000, "lng": 103.7500, "desc": "A parkland course in Johor, featuring water features and strategic design."},
    {"name": "Port Dickson Golf & Country Club", "location": "Port Dickson, Malaysia", "continent": "Asia", "type": "resort", "lat": 2.5200, "lng": 101.8000, "desc": "A coastal resort golf course, offering seaside golf with excellent facilities."},
    {"name": "Rahman Putra Golf Club", "location": "Kuala Lumpur, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.1500, "lng": 101.7000, "desc": "A parkland course in Kuala Lumpur, featuring mature trees and well-designed holes."},
    {"name": "Saujana Golf & Country Club", "location": "Shah Alam, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.0800, "lng": 101.5500, "desc": "A well-regarded golf club near Kuala Lumpur, offering championship-quality parkland courses."},
    {"name": "Seremban Golf Club", "location": "Seremban, Malaysia", "continent": "Asia", "type": "parkland", "lat": 2.7300, "lng": 101.9400, "desc": "A traditional golf club in Seremban, featuring parkland design with mature trees."},
    {"name": "Sungai Long Golf & Country Club", "location": "Kajang, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.0000, "lng": 101.8000, "desc": "A parkland course near Kuala Lumpur, offering tropical golf with strategic water hazards."},
    {"name": "Templer Park Country Club", "location": "Rawang, Malaysia", "continent": "Asia", "type": "parkland", "lat": 3.3200, "lng": 101.5800, "desc": "A parkland course in Selangor, featuring natural terrain and challenging design."},
    {"name": "Tropicana Golf & Country Resort", "location": "Petaling Jaya, Malaysia", "continent": "Asia", "type": "resort", "lat": 3.1000, "lng": 101.6000, "desc": "A resort golf course in Petaling Jaya, offering tropical golf with excellent facilities."},
    
    # Thailand (15 courses)
    {"name": "Alpine Golf Club", "location": "Bangkok, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.7563, "lng": 100.5018, "desc": "A well-regarded parkland course in Bangkok, featuring excellent conditioning and strategic design."},
    {"name": "Blue Canyon Country Club", "location": "Phuket, Thailand", "continent": "Asia", "type": "resort", "lat": 7.8800, "lng": 98.4000, "desc": "A resort golf course in Phuket, offering tropical island golf with stunning views."},
    {"name": "Banyan Golf Club", "location": "Hua Hin, Thailand", "continent": "Asia", "type": "resort", "lat": 12.5700, "lng": 99.9500, "desc": "A resort golf course in Hua Hin, featuring tropical landscaping and well-designed holes."},
    {"name": "Black Mountain Golf Club", "location": "Hua Hin, Thailand", "continent": "Asia", "type": "resort", "lat": 12.5700, "lng": 99.9500, "desc": "A championship resort course in Hua Hin, offering excellent facilities and challenging golf."},
    {"name": "Dusit Thani Laguna Phuket", "location": "Phuket, Thailand", "continent": "Asia", "type": "resort", "lat": 7.8800, "lng": 98.4000, "desc": "A resort golf course in Phuket, offering tropical island golf with excellent maintenance."},
    {"name": "Laem Chabang International Country Club", "location": "Chonburi, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.1000, "lng": 100.9000, "desc": "A well-regarded golf club in Chonburi, featuring multiple courses and excellent facilities."},
    {"name": "Muang Kaew Golf Club", "location": "Bangkok, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.7563, "lng": 100.5018, "desc": "A parkland course in Bangkok, featuring mature trees and strategic water hazards."},
    {"name": "Navy Golf Course", "location": "Sattahip, Thailand", "continent": "Asia", "type": "parkland", "lat": 12.6800, "lng": 100.9000, "desc": "A public golf course in Sattahip, offering accessible golf with good facilities."},
    {"name": "Panya Indra Golf Club", "location": "Bangkok, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.7563, "lng": 100.5018, "desc": "A parkland course in Bangkok, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Phoenix Gold Golf & Country Club", "location": "Pattaya, Thailand", "continent": "Asia", "type": "resort", "lat": 12.9200, "lng": 100.8800, "desc": "A resort golf course in Pattaya, offering tropical golf with excellent facilities."},
    {"name": "Rayong Green Valley Country Club", "location": "Rayong, Thailand", "continent": "Asia", "type": "parkland", "lat": 12.6700, "lng": 101.2800, "desc": "A parkland course in Rayong, featuring water features and strategic design."},
    {"name": "Royal Gems Golf & Sports Club", "location": "Bangkok, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.7563, "lng": 100.5018, "desc": "A premium golf club in Bangkok, offering championship-quality parkland courses."},
    {"name": "Siam Country Club", "location": "Pattaya, Thailand", "continent": "Asia", "type": "parkland", "lat": 12.9200, "lng": 100.8800, "desc": "A well-established golf club in Pattaya, featuring multiple courses and excellent facilities."},
    {"name": "Springfield Royal Country Club", "location": "Hua Hin, Thailand", "continent": "Asia", "type": "resort", "lat": 12.5700, "lng": 99.9500, "desc": "A resort golf course in Hua Hin, offering tropical golf with excellent maintenance."},
    {"name": "Thai Country Club", "location": "Bangkok, Thailand", "continent": "Asia", "type": "parkland", "lat": 13.7563, "lng": 100.5018, "desc": "A prestigious golf club in Bangkok, featuring championship-quality parkland courses."},
    
    # Indonesia (10 courses)
    {"name": "Bumi Serpong Damai Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.3000, "lng": 106.6500, "desc": "A parkland course in Jakarta, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Cengkareng Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A well-regarded golf club in Jakarta, offering championship-quality parkland courses."},
    {"name": "Damai Indah Golf & Country Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A golf club in Jakarta, featuring multiple courses and excellent facilities."},
    {"name": "Emerald Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A parkland course in Jakarta, offering tropical golf with strategic water hazards."},
    {"name": "Jakarta Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A traditional golf club in Jakarta, featuring parkland design with mature trees."},
    {"name": "Pondok Indah Golf & Country Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A well-established golf club in Jakarta, offering excellent facilities and enjoyable parkland golf."},
    {"name": "Rancamaya Golf & Country Club", "location": "Bogor, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.6000, "lng": 106.8000, "desc": "A parkland course in Bogor, featuring natural terrain and challenging design."},
    {"name": "Royale Jakarta Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A premium golf club in Jakarta, offering championship-quality parkland courses."},
    {"name": "Senayan National Golf Club", "location": "Jakarta, Indonesia", "continent": "Asia", "type": "parkland", "lat": -6.2088, "lng": 106.8456, "desc": "A parkland course in central Jakarta, offering accessible golf with good facilities."},
    {"name": "Taman Dayu Golf Club", "location": "Surabaya, Indonesia", "continent": "Asia", "type": "parkland", "lat": -7.2575, "lng": 112.7521, "desc": "A parkland course in Surabaya, featuring tropical landscaping and well-designed holes."},
    
    # Philippines (10 courses)
    {"name": "Alabang Country Club", "location": "Manila, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.4056, "lng": 121.0225, "desc": "A well-established golf club in Manila, offering parkland golf with excellent facilities."},
    {"name": "Canlubang Golf & Country Club", "location": "Laguna, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.2500, "lng": 121.1500, "desc": "A parkland course in Laguna, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Manila Golf & Country Club", "location": "Manila, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.5995, "lng": 120.9842, "desc": "A traditional golf club in Manila, featuring parkland design with mature trees."},
    {"name": "Orchard Golf & Country Club", "location": "Cavite, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.5000, "lng": 120.9000, "desc": "A parkland course in Cavite, offering tropical golf with strategic water hazards."},
    {"name": "Santa Elena Golf & Country Club", "location": "Laguna, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.2500, "lng": 121.1500, "desc": "A well-regarded golf club in Laguna, offering championship-quality parkland courses."},
    {"name": "Tagaytay Highlands Golf Club", "location": "Tagaytay, Philippines", "continent": "Asia", "type": "mountain", "lat": 14.1000, "lng": 120.9300, "desc": "A mountain golf course in Tagaytay, offering cool climate golf with stunning views."},
    {"name": "Wack Wack Golf & Country Club", "location": "Manila, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.5995, "lng": 120.9842, "desc": "A prestigious golf club in Manila, featuring multiple courses and excellent facilities."},
    {"name": "Valley Golf & Country Club", "location": "Antipolo, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.6000, "lng": 121.1000, "desc": "A parkland course in Antipolo, featuring natural terrain and challenging design."},
    {"name": "Villamor Golf Club", "location": "Manila, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.5995, "lng": 120.9842, "desc": "A public golf course in Manila, offering accessible golf with good facilities."},
    {"name": "Southwoods Golf & Country Club", "location": "Laguna, Philippines", "continent": "Asia", "type": "parkland", "lat": 14.2500, "lng": 121.1500, "desc": "A modern golf club in Laguna, featuring well-designed parkland courses with excellent facilities."},
    
    # Vietnam (10 courses)
    {"name": "Chi Linh Star Golf & Country Club", "location": "Hai Duong, Vietnam", "continent": "Asia", "type": "parkland", "lat": 20.9370, "lng": 106.3300, "desc": "A parkland course in Hai Duong, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Dalat Palace Golf Club", "location": "Da Lat, Vietnam", "continent": "Asia", "type": "mountain", "lat": 11.9400, "lng": 108.4400, "desc": "A mountain golf course in Da Lat, offering cool climate golf with stunning mountain views."},
    {"name": "FLC Quy Nhon Golf Links", "location": "Quy Nhon, Vietnam", "continent": "Asia", "type": "coastal", "lat": 13.7700, "lng": 109.2300, "desc": "A coastal golf course in Quy Nhon, offering seaside golf with excellent facilities."},
    {"name": "Hoiana Shores Golf Club", "location": "Hoi An, Vietnam", "continent": "Asia", "type": "coastal", "lat": 15.8800, "lng": 108.3300, "desc": "A coastal golf course in Hoi An, featuring links-style design with ocean views."},
    {"name": "Montgomerie Links Vietnam", "location": "Da Nang, Vietnam", "continent": "Asia", "type": "coastal", "lat": 16.0544, "lng": 108.2022, "desc": "A links-style course in Da Nang, offering seaside golf with challenging winds."},
    {"name": "Phoenix Golf Resort", "location": "Hanoi, Vietnam", "continent": "Asia", "type": "parkland", "lat": 21.0285, "lng": 105.8542, "desc": "A parkland course near Hanoi, featuring tropical landscaping and strategic design."},
    {"name": "Song Be Golf Resort", "location": "Ho Chi Minh City, Vietnam", "continent": "Asia", "type": "parkland", "lat": 10.8231, "lng": 106.6297, "desc": "A parkland course in Ho Chi Minh City, offering tropical golf with water features."},
    {"name": "Tam Dao Golf Resort", "location": "Vinh Phuc, Vietnam", "continent": "Asia", "type": "mountain", "lat": 21.4600, "lng": 105.6500, "desc": "A mountain golf course in Vinh Phuc, offering cool climate golf with scenic views."},
    {"name": "Van Tri Golf Club", "location": "Hanoi, Vietnam", "continent": "Asia", "type": "parkland", "lat": 21.0285, "lng": 105.8542, "desc": "A parkland course near Hanoi, featuring mature trees and well-designed holes."},
    {"name": "Vietnam Golf & Country Club", "location": "Ho Chi Minh City, Vietnam", "continent": "Asia", "type": "parkland", "lat": 10.8231, "lng": 106.6297, "desc": "A well-regarded golf club in Ho Chi Minh City, offering championship-quality parkland courses."},
    
    # Europe - France (10 courses)
    {"name": "Golf de Chantilly", "location": "Chantilly, France", "continent": "Europe", "type": "parkland", "lat": 49.1940, "lng": 2.4700, "desc": "A historic parkland course near Paris, featuring classic French golf course design."},
    {"name": "Golf de Fontainebleau", "location": "Fontainebleau, France", "continent": "Europe", "type": "parkland", "lat": 48.4000, "lng": 2.7000, "desc": "A parkland course in the forest of Fontainebleau, offering natural and challenging golf."},
    {"name": "Golf de La Grande Motte", "location": "La Grande Motte, France", "continent": "Europe", "type": "coastal", "lat": 43.5600, "lng": 4.0900, "desc": "A coastal golf course on the French Riviera, offering seaside golf with Mediterranean views."},
    {"name": "Golf de Lyon", "location": "Lyon, France", "continent": "Europe", "type": "parkland", "lat": 45.7640, "lng": 4.8357, "desc": "A parkland course in Lyon, featuring mature trees and strategic design."},
    {"name": "Golf de Morfontaine", "location": "Mortefontaine, France", "continent": "Europe", "type": "parkland", "lat": 49.1100, "lng": 2.6000, "desc": "A well-regarded parkland course near Paris, offering classic French golf architecture."},
    {"name": "Golf de Saint-Cloud", "location": "Saint-Cloud, France", "continent": "Europe", "type": "parkland", "lat": 48.8500, "lng": 2.2200, "desc": "A parkland course near Paris, featuring excellent conditioning and strategic design."},
    {"name": "Golf de Seignosse", "location": "Seignosse, France", "continent": "Europe", "type": "links", "lat": 43.6900, "lng": -1.3700, "desc": "A links-style course on the Atlantic coast, offering authentic seaside golf."},
    {"name": "Golf du Médoc", "location": "Bordeaux, France", "continent": "Europe", "type": "parkland", "lat": 44.8378, "lng": -0.5792, "desc": "A parkland course in the Bordeaux region, featuring wine country scenery."},
    {"name": "Golf International de Pont Royal", "location": "Mallemort, France", "continent": "Europe", "type": "parkland", "lat": 43.7300, "lng": 5.1800, "desc": "A parkland course in Provence, offering Mediterranean golf with excellent facilities."},
    {"name": "Le Golf National", "location": "Paris, France", "continent": "Europe", "type": "championship", "lat": 48.8566, "lng": 2.3522, "desc": "A championship course near Paris, featuring modern design and excellent conditioning."},
    
    # Europe - Germany (10 courses)
    {"name": "Golf Club Bad Saarow", "location": "Bad Saarow, Germany", "continent": "Europe", "type": "parkland", "lat": 52.2800, "lng": 14.0600, "desc": "A parkland course in Brandenburg, featuring lakes and mature trees."},
    {"name": "Golf Club Gut Lärchenhof", "location": "Pulheim, Germany", "continent": "Europe", "type": "parkland", "lat": 50.9600, "lng": 6.8000, "desc": "A well-regarded parkland course near Cologne, offering excellent conditioning."},
    {"name": "Golf Club St. Leon-Rot", "location": "St. Leon-Rot, Germany", "continent": "Europe", "type": "parkland", "lat": 49.2600, "lng": 8.6100, "desc": "A championship parkland course in Baden-Württemberg, featuring modern design."},
    {"name": "Golf Club München Eichenried", "location": "Munich, Germany", "continent": "Europe", "type": "parkland", "lat": 48.1351, "lng": 11.5820, "desc": "A parkland course near Munich, offering excellent facilities and enjoyable golf."},
    {"name": "Golf Resort Achental", "location": "Grassau, Germany", "continent": "Europe", "type": "mountain", "lat": 47.7800, "lng": 12.4300, "desc": "A mountain golf course in the Bavarian Alps, offering stunning alpine views."},
    {"name": "Golf und Land-Club Köln", "location": "Cologne, Germany", "continent": "Europe", "type": "parkland", "lat": 50.9375, "lng": 6.9603, "desc": "A traditional parkland course in Cologne, featuring classic German golf design."},
    {"name": "Hamburger Golf Club", "location": "Hamburg, Germany", "continent": "Europe", "type": "parkland", "lat": 53.5511, "lng": 9.9937, "desc": "A parkland course in Hamburg, offering excellent conditioning and strategic design."},
    {"name": "Golf Club Berlin-Wannsee", "location": "Berlin, Germany", "continent": "Europe", "type": "parkland", "lat": 52.5200, "lng": 13.4050, "desc": "A historic parkland course in Berlin, featuring mature trees and traditional design."},
    {"name": "Golf Club Hubbelrath", "location": "Düsseldorf, Germany", "continent": "Europe", "type": "parkland", "lat": 51.2277, "lng": 6.7735, "desc": "A parkland course near Düsseldorf, offering good value and enjoyable golf."},
    {"name": "Golf Resort Fleesensee", "location": "Göhren-Lebbin, Germany", "continent": "Europe", "type": "parkland", "lat": 53.4800, "lng": 12.5000, "desc": "A resort golf course in Mecklenburg, featuring lakes and natural terrain."},
    
    # Europe - Spain (10 courses)
    {"name": "Club de Golf El Prat", "location": "Barcelona, Spain", "continent": "Europe", "type": "parkland", "lat": 41.3851, "lng": 2.1734, "desc": "A well-regarded parkland course near Barcelona, offering excellent facilities."},
    {"name": "Golf Costa Adeje", "location": "Tenerife, Spain", "continent": "Europe", "type": "coastal", "lat": 28.1000, "lng": -16.7167, "desc": "A coastal golf course in Tenerife, offering year-round golf with ocean views."},
    {"name": "Golf de Son Servera", "location": "Mallorca, Spain", "continent": "Europe", "type": "coastal", "lat": 39.5700, "lng": 3.2000, "desc": "A coastal golf course in Mallorca, featuring Mediterranean views and excellent conditioning."},
    {"name": "Golf Las Ramblas", "location": "Alicante, Spain", "continent": "Europe", "type": "parkland", "lat": 38.3452, "lng": -0.4810, "desc": "A parkland course in Alicante, offering year-round golf with good facilities."},
    {"name": "Golf Santander", "location": "Santander, Spain", "continent": "Europe", "type": "coastal", "lat": 43.4623, "lng": -3.8099, "desc": "A coastal golf course in northern Spain, offering seaside golf with Atlantic views."},
    {"name": "La Manga Club", "location": "Murcia, Spain", "continent": "Europe", "type": "resort", "lat": 37.6000, "lng": -0.9833, "desc": "A resort golf complex in Murcia, featuring multiple courses and excellent facilities."},
    {"name": "PGA Catalunya Resort", "location": "Girona, Spain", "continent": "Europe", "type": "parkland", "lat": 41.9794, "lng": 2.8214, "desc": "A championship golf resort near Barcelona, offering world-class facilities."},
    {"name": "Real Club de Golf El Prat", "location": "Barcelona, Spain", "continent": "Europe", "type": "parkland", "lat": 41.3851, "lng": 2.1734, "desc": "A prestigious golf club near Barcelona, featuring championship-quality courses."},
    {"name": "Valderrama Golf Club", "location": "Sotogrande, Spain", "continent": "Europe", "type": "championship", "lat": 36.2833, "lng": -5.3000, "desc": "A championship course in Sotogrande, known for hosting major tournaments."},
    {"name": "Villa Padierna Golf Club", "location": "Marbella, Spain", "continent": "Europe", "type": "resort", "lat": 36.5100, "lng": -4.8856, "desc": "A resort golf course in Marbella, offering Mediterranean golf with excellent facilities."},
    
    # Europe - Italy (10 courses)
    {"name": "Circolo Golf Villa d'Este", "location": "Como, Italy", "continent": "Europe", "type": "parkland", "lat": 45.8081, "lng": 9.0852, "desc": "A scenic parkland course on Lake Como, offering stunning alpine and lake views."},
    {"name": "Golf Club Biella", "location": "Biella, Italy", "continent": "Europe", "type": "parkland", "lat": 45.5700, "lng": 8.0500, "desc": "A parkland course in northern Italy, featuring mountain views and strategic design."},
    {"name": "Golf Club Castelconturbia", "location": "Novara, Italy", "continent": "Europe", "type": "parkland", "lat": 45.4500, "lng": 8.6200, "desc": "A well-regarded parkland course in northern Italy, offering excellent conditioning."},
    {"name": "Golf Club Milano", "location": "Milan, Italy", "continent": "Europe", "type": "parkland", "lat": 45.4642, "lng": 9.1900, "desc": "A parkland course near Milan, featuring mature trees and strategic design."},
    {"name": "Golf Club Poggio dei Medici", "location": "Tuscany, Italy", "continent": "Europe", "type": "parkland", "lat": 43.7696, "lng": 11.2558, "desc": "A parkland course in Tuscany, offering beautiful countryside views and excellent golf."},
    {"name": "Golf Nazionale", "location": "Rome, Italy", "continent": "Europe", "type": "parkland", "lat": 41.9028, "lng": 12.4964, "desc": "A parkland course near Rome, featuring classic Italian golf design."},
    {"name": "Is Molas Golf Club", "location": "Sardinia, Italy", "continent": "Europe", "type": "coastal", "lat": 39.2000, "lng": 9.1000, "desc": "A coastal golf course in Sardinia, offering Mediterranean golf with stunning views."},
    {"name": "Marco Simone Golf & Country Club", "location": "Rome, Italy", "continent": "Europe", "type": "championship", "lat": 41.9028, "lng": 12.4964, "desc": "A championship course near Rome, featuring modern design and excellent facilities."},
    {"name": "Olgiata Golf Club", "location": "Rome, Italy", "continent": "Europe", "type": "parkland", "lat": 41.9028, "lng": 12.4964, "desc": "A parkland course near Rome, offering excellent conditioning and strategic design."},
    {"name": "Verona Golf Club", "location": "Verona, Italy", "continent": "Europe", "type": "parkland", "lat": 45.4384, "lng": 10.9916, "desc": "A parkland course in Verona, featuring beautiful Italian countryside scenery."},
    
    # South America (15 courses)
    {"name": "Golf Club Los Leones", "location": "Santiago, Chile", "continent": "South America", "type": "parkland", "lat": -33.4489, "lng": -70.6693, "desc": "A parkland course in Santiago, featuring mountain views and excellent conditioning."},
    {"name": "Golf Club de Medellín", "location": "Medellín, Colombia", "continent": "South America", "type": "mountain", "lat": 6.2476, "lng": -75.5658, "desc": "A mountain golf course in Medellín, offering cool climate golf with scenic views."},
    {"name": "Golf Club do Rio de Janeiro", "location": "Rio de Janeiro, Brazil", "continent": "South America", "type": "parkland", "lat": -22.9068, "lng": -43.1729, "desc": "A parkland course in Rio de Janeiro, offering tropical golf with excellent facilities."},
    {"name": "Golf Club San Andrés", "location": "Buenos Aires, Argentina", "continent": "South America", "type": "parkland", "lat": -34.6037, "lng": -58.3816, "desc": "A parkland course in Buenos Aires, featuring mature trees and strategic design."},
    {"name": "Jockey Club de São Paulo", "location": "São Paulo, Brazil", "continent": "South America", "type": "parkland", "lat": -23.5505, "lng": -46.6333, "desc": "A prestigious golf club in São Paulo, offering championship-quality parkland courses."},
    {"name": "Los Inkas Golf Club", "location": "Lima, Peru", "continent": "South America", "type": "parkland", "lat": -12.0464, "lng": -77.0428, "desc": "A parkland course in Lima, featuring desert landscaping and strategic design."},
    {"name": "Olivos Golf Club", "location": "Buenos Aires, Argentina", "continent": "South America", "type": "parkland", "lat": -34.6037, "lng": -58.3816, "desc": "A well-regarded parkland course in Buenos Aires, offering excellent conditioning."},
    {"name": "Pilará Golf Club", "location": "Buenos Aires, Argentina", "continent": "South America", "type": "parkland", "lat": -34.6037, "lng": -58.3816, "desc": "A parkland course near Buenos Aires, featuring modern design and excellent facilities."},
    {"name": "Quinta da Baroneza Golf Club", "location": "São Paulo, Brazil", "continent": "South America", "type": "parkland", "lat": -23.5505, "lng": -46.6333, "desc": "A parkland course in São Paulo, offering tropical golf with strategic water hazards."},
    {"name": "San Isidro Golf Club", "location": "Buenos Aires, Argentina", "continent": "South America", "type": "parkland", "lat": -34.6037, "lng": -58.3816, "desc": "A traditional golf club in Buenos Aires, featuring parkland design with mature trees."},
    {"name": "Terravista Golf Club", "location": "Trancoso, Brazil", "continent": "South America", "type": "coastal", "lat": -16.6500, "lng": -39.1000, "desc": "A coastal golf course in Bahia, offering seaside golf with Atlantic views."},
    {"name": "Valle del Sol Golf Club", "location": "Santiago, Chile", "continent": "South America", "type": "parkland", "lat": -33.4489, "lng": -70.6693, "desc": "A parkland course in Santiago, featuring mountain views and excellent conditioning."},
    {"name": "Villa Allende Golf Club", "location": "Córdoba, Argentina", "continent": "South America", "type": "parkland", "lat": -31.4201, "lng": -64.1888, "desc": "A parkland course in Córdoba, offering mountain views and strategic design."},
    {"name": "Yacht & Golf Club Paraguayo", "location": "Asunción, Paraguay", "continent": "South America", "type": "parkland", "lat": -25.2637, "lng": -57.5759, "desc": "A parkland course in Asunción, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Zapallar Golf Club", "location": "Zapallar, Chile", "continent": "South America", "type": "coastal", "lat": -32.5500, "lng": -71.4500, "desc": "A coastal golf course in central Chile, offering Pacific views and challenging seaside golf."},
    
    # Africa (15 courses)
    {"name": "Arabella Golf Club", "location": "Cape Town, South Africa", "continent": "Africa", "type": "parkland", "lat": -33.9249, "lng": 18.4241, "desc": "A parkland course near Cape Town, featuring lagoon views and strategic design."},
    {"name": "Durban Country Club", "location": "Durban, South Africa", "continent": "Africa", "type": "coastal", "lat": -29.8587, "lng": 31.0218, "desc": "A coastal golf course in Durban, offering Indian Ocean views and excellent conditioning."},
    {"name": "Fancourt Golf Estate", "location": "George, South Africa", "continent": "Africa", "type": "parkland", "lat": -33.9667, "lng": 22.4500, "desc": "A well-regarded golf estate in George, featuring multiple courses and excellent facilities."},
    {"name": "Glendower Golf Club", "location": "Johannesburg, South Africa", "continent": "Africa", "type": "parkland", "lat": -26.2041, "lng": 28.0473, "desc": "A parkland course in Johannesburg, offering excellent conditioning and strategic design."},
    {"name": "Leopard Creek Country Club", "location": "Mpumalanga, South Africa", "continent": "Africa", "type": "parkland", "lat": -25.5000, "lng": 31.5000, "desc": "A parkland course near Kruger National Park, featuring wildlife and natural terrain."},
    {"name": "Royal Johannesburg & Kensington Golf Club", "location": "Johannesburg, South Africa", "continent": "Africa", "type": "parkland", "lat": -26.2041, "lng": 28.0473, "desc": "A prestigious golf club in Johannesburg, featuring multiple courses and excellent facilities."},
    {"name": "Steenberg Golf Club", "location": "Cape Town, South Africa", "continent": "Africa", "type": "parkland", "lat": -33.9249, "lng": 18.4241, "desc": "A parkland course in Cape Town, featuring mountain views and excellent conditioning."},
    {"name": "Sun City Golf Club", "location": "Sun City, South Africa", "continent": "Africa", "type": "resort", "lat": -25.3300, "lng": 27.1000, "desc": "A resort golf course in Sun City, offering excellent facilities and enjoyable golf."},
    {"name": "The Links at Fancourt", "location": "George, South Africa", "continent": "Africa", "type": "parkland", "lat": -33.9667, "lng": 22.4500, "desc": "A links-style course in George, offering challenging golf with excellent conditioning."},
    {"name": "Zimbali Country Club", "location": "Ballito, South Africa", "continent": "Africa", "type": "coastal", "lat": -29.5000, "lng": 31.2000, "desc": "A coastal golf course in Ballito, offering Indian Ocean views and tropical golf."},
    {"name": "Royal Dar es Salaam Golf Club", "location": "Dar es Salaam, Tanzania", "continent": "Africa", "type": "parkland", "lat": -6.7924, "lng": 39.2083, "desc": "A parkland course in Dar es Salaam, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Karen Country Club", "location": "Nairobi, Kenya", "continent": "Africa", "type": "parkland", "lat": -1.2921, "lng": 36.8219, "desc": "A parkland course in Nairobi, offering excellent facilities and enjoyable golf."},
    {"name": "Ain Sokhna Golf Club", "location": "Ain Sokhna, Egypt", "continent": "Africa", "type": "coastal", "lat": 29.6000, "lng": 32.3000, "desc": "A coastal golf course on the Red Sea, offering desert and sea views."},
    {"name": "Jumeirah Golf Estates", "location": "Dubai, UAE", "continent": "Middle East", "type": "parkland", "lat": 25.0657, "lng": 55.1713, "desc": "A modern golf estate in Dubai, featuring championship courses and excellent facilities."},
    {"name": "Abu Dhabi Golf Club", "location": "Abu Dhabi, UAE", "continent": "Middle East", "type": "parkland", "lat": 24.4539, "lng": 54.3773, "desc": "A championship golf club in Abu Dhabi, offering desert golf with excellent conditioning."},
    
    # Middle East (10 courses)
    {"name": "Doha Golf Club", "location": "Doha, Qatar", "continent": "Middle East", "type": "parkland", "lat": 25.2854, "lng": 51.5310, "desc": "A parkland course in Doha, featuring desert landscaping and excellent facilities."},
    {"name": "Emirates Golf Club", "location": "Dubai, UAE", "continent": "Middle East", "type": "parkland", "lat": 25.0657, "lng": 55.1713, "desc": "A well-regarded golf club in Dubai, offering championship-quality desert courses."},
    {"name": "Yas Links Abu Dhabi", "location": "Abu Dhabi, UAE", "continent": "Middle East", "type": "coastal", "lat": 24.4539, "lng": 54.3773, "desc": "A links-style course in Abu Dhabi, offering seaside golf with excellent conditioning."},
    {"name": "Royal Golf Club Bahrain", "location": "Manama, Bahrain", "continent": "Middle East", "type": "parkland", "lat": 26.0667, "lng": 50.5577, "desc": "A parkland course in Bahrain, featuring desert landscaping and strategic design."},
    {"name": "Dubai Creek Golf & Yacht Club", "location": "Dubai, UAE", "continent": "Middle East", "type": "parkland", "lat": 25.0657, "lng": 55.1713, "desc": "A parkland course in Dubai, offering city views and excellent facilities."},
    {"name": "Al Zorah Golf Club", "location": "Ajman, UAE", "continent": "Middle East", "type": "coastal", "lat": 25.4052, "lng": 55.5136, "desc": "A coastal golf course in Ajman, offering Arabian Gulf views and challenging golf."},
    {"name": "Saudi Golf Club", "location": "Riyadh, Saudi Arabia", "continent": "Middle East", "type": "parkland", "lat": 24.7136, "lng": 46.6753, "desc": "A parkland course in Riyadh, featuring desert landscaping and excellent facilities."},
    {"name": "King Abdullah Economic City Golf Club", "location": "Jeddah, Saudi Arabia", "continent": "Middle East", "type": "coastal", "lat": 21.4858, "lng": 39.1925, "desc": "A coastal golf course in Jeddah, offering Red Sea views and modern design."},
    {"name": "Muscat Hills Golf & Country Club", "location": "Muscat, Oman", "continent": "Middle East", "type": "coastal", "lat": 23.5859, "lng": 58.4059, "desc": "A coastal golf course in Muscat, offering Arabian Sea views and excellent facilities."},
    {"name": "Dirab Golf & Country Club", "location": "Riyadh, Saudi Arabia", "continent": "Middle East", "type": "parkland", "lat": 24.7136, "lng": 46.6753, "desc": "A parkland course in Riyadh, featuring desert landscaping and strategic design."},
    
    # Additional courses to reach 250 (remaining 35 courses from various regions)
    {"name": "Auckland Golf Club", "location": "Auckland, New Zealand", "continent": "Oceania", "type": "parkland", "lat": -36.8485, "lng": 174.7633, "desc": "A parkland course in Auckland, offering excellent conditioning and strategic design."},
    {"name": "Christchurch Golf Club", "location": "Christchurch, New Zealand", "continent": "Oceania", "type": "parkland", "lat": -43.5321, "lng": 172.6362, "desc": "A parkland course in Christchurch, featuring mature trees and well-maintained fairways."},
    {"name": "Wellington Golf Club", "location": "Wellington, New Zealand", "continent": "Oceania", "type": "parkland", "lat": -41.2865, "lng": 174.7762, "desc": "A parkland course in Wellington, offering scenic views and enjoyable golf."},
    {"name": "Royal Melbourne Golf Club", "location": "Melbourne, Australia", "continent": "Oceania", "type": "parkland", "lat": -37.8136, "lng": 144.9631, "desc": "A well-regarded parkland course in Melbourne, offering excellent facilities."},
    {"name": "Royal Sydney Golf Club", "location": "Sydney, Australia", "continent": "Oceania", "type": "parkland", "lat": -33.8688, "lng": 151.2093, "desc": "A prestigious golf club in Sydney, featuring championship-quality courses."},
    {"name": "Perth Golf Club", "location": "Perth, Australia", "continent": "Oceania", "type": "parkland", "lat": -31.9505, "lng": 115.8605, "desc": "A parkland course in Perth, offering excellent conditioning and strategic design."},
    {"name": "Adelaide Golf Club", "location": "Adelaide, Australia", "continent": "Oceania", "type": "parkland", "lat": -34.9285, "lng": 138.6007, "desc": "A parkland course in Adelaide, featuring mature trees and well-designed holes."},
    {"name": "Brisbane Golf Club", "location": "Brisbane, Australia", "continent": "Oceania", "type": "parkland", "lat": -27.4698, "lng": 153.0251, "desc": "A parkland course in Brisbane, offering tropical golf with excellent facilities."},
    {"name": "Canberra Golf Club", "location": "Canberra, Australia", "continent": "Oceania", "type": "parkland", "lat": -35.2809, "lng": 149.1300, "desc": "A parkland course in Canberra, featuring mountain views and strategic design."},
    {"name": "Hobart Golf Club", "location": "Hobart, Australia", "continent": "Oceania", "type": "parkland", "lat": -42.8821, "lng": 147.3272, "desc": "A parkland course in Hobart, offering scenic views and enjoyable golf."},
    {"name": "Darwin Golf Club", "location": "Darwin, Australia", "continent": "Oceania", "type": "parkland", "lat": -12.4634, "lng": 130.8456, "desc": "A parkland course in Darwin, offering tropical golf with excellent facilities."},
    {"name": "Gold Coast Golf Club", "location": "Gold Coast, Australia", "continent": "Oceania", "type": "coastal", "lat": -28.0167, "lng": 153.4000, "desc": "A coastal golf course on the Gold Coast, offering Pacific views and excellent conditioning."},
    {"name": "Cairns Golf Club", "location": "Cairns, Australia", "continent": "Oceania", "type": "parkland", "lat": -16.9186, "lng": 145.7781, "desc": "A parkland course in Cairns, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Townsville Golf Club", "location": "Townsville, Australia", "continent": "Oceania", "type": "parkland", "lat": -19.2590, "lng": 146.8169, "desc": "A parkland course in Townsville, offering tropical golf with strategic design."},
    {"name": "Toowoomba Golf Club", "location": "Toowoomba, Australia", "continent": "Oceania", "type": "parkland", "lat": -27.5598, "lng": 151.9507, "desc": "A parkland course in Toowoomba, featuring mountain views and excellent conditioning."},
    {"name": "Ballarat Golf Club", "location": "Ballarat, Australia", "continent": "Oceania", "type": "parkland", "lat": -37.5622, "lng": 143.8503, "desc": "A parkland course in Ballarat, offering excellent facilities and enjoyable golf."},
    {"name": "Bendigo Golf Club", "location": "Bendigo, Australia", "continent": "Oceania", "type": "parkland", "lat": -36.7570, "lng": 144.2790, "desc": "A parkland course in Bendigo, featuring mature trees and strategic design."},
    {"name": "Geelong Golf Club", "location": "Geelong, Australia", "continent": "Oceania", "type": "parkland", "lat": -38.1499, "lng": 144.3617, "desc": "A parkland course in Geelong, offering coastal views and excellent conditioning."},
    {"name": "Wollongong Golf Club", "location": "Wollongong, Australia", "continent": "Oceania", "type": "coastal", "lat": -34.4278, "lng": 150.8931, "desc": "A coastal golf course in Wollongong, offering Pacific views and challenging seaside golf."},
    {"name": "Newcastle Golf Club", "location": "Newcastle, Australia", "continent": "Oceania", "type": "coastal", "lat": -32.9283, "lng": 151.7817, "desc": "A coastal golf course in Newcastle, offering excellent facilities and enjoyable golf."},
    {"name": "Albury Golf Club", "location": "Albury, Australia", "continent": "Oceania", "type": "parkland", "lat": -36.0737, "lng": 146.9135, "desc": "A parkland course in Albury, featuring river views and strategic design."},
    {"name": "Wagga Wagga Golf Club", "location": "Wagga Wagga, Australia", "continent": "Oceania", "type": "parkland", "lat": -35.1085, "lng": 147.3598, "desc": "A parkland course in Wagga Wagga, offering excellent conditioning and enjoyable golf."},
    {"name": "Orange Golf Club", "location": "Orange, Australia", "continent": "Oceania", "type": "parkland", "lat": -33.2839, "lng": 149.1000, "desc": "A parkland course in Orange, featuring mountain views and well-maintained fairways."},
    {"name": "Dubbo Golf Club", "location": "Dubbo, Australia", "continent": "Oceania", "type": "parkland", "lat": -32.2472, "lng": 148.6048, "desc": "A parkland course in Dubbo, offering excellent facilities and strategic design."},
    {"name": "Tamworth Golf Club", "location": "Tamworth, Australia", "continent": "Oceania", "type": "parkland", "lat": -31.0906, "lng": 150.9297, "desc": "A parkland course in Tamworth, featuring mature trees and challenging greens."},
    {"name": "Coffs Harbour Golf Club", "location": "Coffs Harbour, Australia", "continent": "Oceania", "type": "coastal", "lat": -30.2963, "lng": 153.1135, "desc": "A coastal golf course in Coffs Harbour, offering Pacific views and excellent conditioning."},
    {"name": "Port Macquarie Golf Club", "location": "Port Macquarie, Australia", "continent": "Oceania", "type": "coastal", "lat": -31.4308, "lng": 152.9089, "desc": "A coastal golf course in Port Macquarie, offering seaside golf with excellent facilities."},
    {"name": "Lismore Golf Club", "location": "Lismore, Australia", "continent": "Oceania", "type": "parkland", "lat": -28.8135, "lng": 153.2773, "desc": "A parkland course in Lismore, featuring tropical landscaping and well-maintained fairways."},
    {"name": "Grafton Golf Club", "location": "Grafton, Australia", "continent": "Oceania", "type": "parkland", "lat": -29.6910, "lng": 152.9339, "desc": "A parkland course in Grafton, offering river views and strategic design."},
    {"name": "Byron Bay Golf Club", "location": "Byron Bay, Australia", "continent": "Oceania", "type": "coastal", "lat": -28.6474, "lng": 153.6020, "desc": "A coastal golf course in Byron Bay, offering Pacific views and challenging seaside golf."},
    {"name": "Tweed Heads Golf Club", "location": "Tweed Heads, Australia", "continent": "Oceania", "type": "coastal", "lat": -28.1750, "lng": 153.5369, "desc": "A coastal golf course in Tweed Heads, offering excellent facilities and enjoyable golf."},
    
    # Additional courses to reach 250 (35 more courses)
    {"name": "Belfast Golf Club", "location": "Belfast, Northern Ireland", "continent": "Europe", "type": "parkland", "lat": 54.5973, "lng": -5.9301, "desc": "A parkland course in Belfast, featuring mature trees and well-maintained fairways."},
    {"name": "Royal Portrush Golf Club", "location": "Portrush, Northern Ireland", "continent": "Europe", "type": "links", "lat": 55.2000, "lng": -6.6500, "desc": "A classic links course on the Northern Ireland coast, offering authentic seaside golf."},
    {"name": "Portstewart Golf Club", "location": "Portstewart, Northern Ireland", "continent": "Europe", "type": "links", "lat": 55.1800, "lng": -6.7200, "desc": "A links course on the Causeway Coast, featuring dunes and challenging coastal winds."},
    {"name": "Castlerock Golf Club", "location": "Castlerock, Northern Ireland", "continent": "Europe", "type": "links", "lat": 55.1500, "lng": -6.7800, "desc": "A traditional links course in Northern Ireland, offering classic seaside golf."},
    {"name": "Royal County Down Golf Club", "location": "Newcastle, Northern Ireland", "continent": "Europe", "type": "links", "lat": 54.2100, "lng": -5.8800, "desc": "A world-renowned links course in Northern Ireland, featuring stunning mountain and sea views."},
    {"name": "Bangor Golf Club", "location": "Bangor, Northern Ireland", "continent": "Europe", "type": "parkland", "lat": 54.6500, "lng": -5.6700, "desc": "A parkland course in Bangor, offering scenic views and enjoyable golf."},
    {"name": "Malone Golf Club", "location": "Belfast, Northern Ireland", "continent": "Europe", "type": "parkland", "lat": 54.5973, "lng": -5.9301, "desc": "A well-established parkland course in Belfast, featuring excellent conditioning."},
    {"name": "Shandon Park Golf Club", "location": "Belfast, Northern Ireland", "continent": "Europe", "type": "parkland", "lat": 54.5973, "lng": -5.9301, "desc": "A parkland course in Belfast, offering good value and enjoyable golf."},
    {"name": "Clandeboye Golf Club", "location": "Bangor, Northern Ireland", "continent": "Europe", "type": "parkland", "lat": 54.6500, "lng": -5.6700, "desc": "A parkland course in Bangor, featuring mature trees and strategic design."},
    {"name": "Dundonald Links", "location": "Dundonald, Scotland", "continent": "Europe", "type": "links", "lat": 55.5700, "lng": -4.6000, "desc": "A modern links course in Ayrshire, offering championship-quality seaside golf."},
    {"name": "Gullane Golf Club", "location": "Gullane, Scotland", "continent": "Europe", "type": "links", "lat": 56.0300, "lng": -2.8300, "desc": "A classic links course in East Lothian, featuring multiple courses and excellent facilities."},
    {"name": "Kilspindie Golf Club", "location": "Aberlady, Scotland", "continent": "Europe", "type": "links", "lat": 56.0100, "lng": -2.8600, "desc": "A traditional links course in East Lothian, offering authentic Scottish seaside golf."},
    {"name": "Luffness New Golf Club", "location": "Aberlady, Scotland", "continent": "Europe", "type": "links", "lat": 56.0100, "lng": -2.8600, "desc": "A links course in East Lothian, featuring firm fairways and challenging bunkers."},
    {"name": "Muirfield", "location": "Gullane, Scotland", "continent": "Europe", "type": "links", "lat": 56.0300, "lng": -2.8300, "desc": "A prestigious links course in East Lothian, known for hosting The Open Championship."},
    {"name": "North Berwick Golf Club", "location": "North Berwick, Scotland", "continent": "Europe", "type": "links", "lat": 56.0600, "lng": -2.7200, "desc": "A historic links course in East Lothian, offering classic Scottish seaside golf."},
    {"name": "Prestwick Golf Club", "location": "Prestwick, Scotland", "continent": "Europe", "type": "links", "lat": 55.5000, "lng": -4.6100, "desc": "A historic links course in Ayrshire, where The Open Championship was first played."},
    {"name": "Royal Troon Golf Club", "location": "Troon, Scotland", "continent": "Europe", "type": "links", "lat": 55.5400, "lng": -4.6500, "desc": "A championship links course in Ayrshire, featuring multiple Open Championship venues."},
    {"name": "Turnberry Golf Club", "location": "Turnberry, Scotland", "continent": "Europe", "type": "links", "lat": 55.3200, "lng": -4.8300, "desc": "A world-renowned links course in Ayrshire, offering stunning coastal views."},
    {"name": "Western Gailes Golf Club", "location": "Irvine, Scotland", "continent": "Europe", "type": "links", "lat": 55.6000, "lng": -4.6500, "desc": "A classic links course in Ayrshire, featuring natural dunes and challenging winds."},
    {"name": "Machrihanish Golf Club", "location": "Campbeltown, Scotland", "continent": "Europe", "type": "links", "lat": 55.4200, "lng": -5.7000, "desc": "A remote links course on the Kintyre Peninsula, offering authentic Scottish golf."},
    {"name": "Machrie Golf Links", "location": "Islay, Scotland", "continent": "Europe", "type": "links", "lat": 55.8000, "lng": -6.2000, "desc": "A links course on the Isle of Islay, offering remote and challenging seaside golf."},
    {"name": "Askernish Golf Club", "location": "South Uist, Scotland", "continent": "Europe", "type": "links", "lat": 57.2000, "lng": -7.4000, "desc": "A remote links course in the Outer Hebrides, offering wild and natural golf."},
    {"name": "Brora Golf Club", "location": "Brora, Scotland", "continent": "Europe", "type": "links", "lat": 58.0100, "lng": -3.8500, "desc": "A links course in the Scottish Highlands, featuring traditional design and coastal views."},
    {"name": "Golspie Golf Club", "location": "Golspie, Scotland", "continent": "Europe", "type": "links", "lat": 57.9700, "lng": -3.9800, "desc": "A links course in the Scottish Highlands, offering scenic views and enjoyable golf."},
    {"name": "Tain Golf Club", "location": "Tain, Scotland", "continent": "Europe", "type": "links", "lat": 57.8100, "lng": -4.0500, "desc": "A traditional links course in the Scottish Highlands, featuring classic design."},
    {"name": "Fortrose & Rosemarkie Golf Club", "location": "Fortrose, Scotland", "continent": "Europe", "type": "links", "lat": 57.5800, "lng": -4.1300, "desc": "A links course on the Black Isle, offering scenic views and challenging golf."},
    {"name": "Nairn Golf Club", "location": "Nairn, Scotland", "continent": "Europe", "type": "links", "lat": 57.5800, "lng": -3.8700, "desc": "A well-regarded links course in the Scottish Highlands, featuring excellent conditioning."},
    {"name": "Royal Dornoch Golf Club", "location": "Dornoch, Scotland", "continent": "Europe", "type": "links", "lat": 57.8800, "lng": -4.0300, "desc": "A world-renowned links course in the Scottish Highlands, offering classic seaside golf."},
    {"name": "Wick Golf Club", "location": "Wick, Scotland", "continent": "Europe", "type": "links", "lat": 58.4400, "lng": -3.0900, "desc": "A links course in the far north of Scotland, offering remote and challenging golf."},
    {"name": "Lybster Golf Club", "location": "Lybster, Scotland", "continent": "Europe", "type": "links", "lat": 58.3000, "lng": -3.2800, "desc": "A links course in Caithness, featuring natural terrain and coastal views."},
    {"name": "Reay Golf Club", "location": "Reay, Scotland", "continent": "Europe", "type": "links", "lat": 58.5500, "lng": -3.7800, "desc": "A links course in the far north of Scotland, offering authentic seaside golf."},
    {"name": "Thurso Golf Club", "location": "Thurso, Scotland", "continent": "Europe", "type": "links", "lat": 58.5900, "lng": -3.5200, "desc": "A links course in the far north of Scotland, featuring challenging coastal winds."},
    {"name": "Durness Golf Club", "location": "Durness, Scotland", "continent": "Europe", "type": "links", "lat": 58.5700, "lng": -4.7500, "desc": "A remote links course in the far north of Scotland, offering wild and natural golf."},
]

def generate_course_id(name):
    """Generate a URL-friendly ID from course name"""
    # Convert to lowercase and replace spaces/special chars with hyphens
    course_id = re.sub(r'[^a-z0-9]+', '-', name.lower())
    # Remove leading/trailing hyphens
    course_id = course_id.strip('-')
    # Add igolf prefix to avoid conflicts
    return f"igolf-{course_id}"

def create_igolf_course(course_data, index):
    """Create an igolf course entry"""
    course_id = generate_course_id(course_data["name"])
    
    # Generate rating between 3.0 and 3.8
    import random
    random.seed(course_id)  # For consistency
    rating = round(random.uniform(3.0, 3.8), 1)
    
    # Generate yardage between 6000 and 6800
    yardage = random.randint(6000, 6800)
    
    return {
        "id": course_id,
        "name": course_data["name"],
        "description": course_data["desc"],
        "location": course_data["location"],
        "rating": rating,
        "category": "igolf",
        "type": course_data["type"],
        "continent": course_data["continent"],
        "latitude": course_data["lat"],
        "longitude": course_data["lng"],
        "yardage": yardage,
        "isIgolf": True,
        "hasImage": False,
        "isStudio": False,
        "hasStandardVersion": False,
        "blurb": [course_data["desc"]],  # Single paragraph in blurb array
        "igolfFeatures": {
            "mappingType": "Radar",
            "accuracy": "+/-5m",
            "resolution": "Standard",
            "physics": "Basic Terrain Model",
            "fileSize": "200 MB"
        },
        "images": {
            "hero": None,
            "additional": []
        },
        "imageUrl": None
    }

def main():
    print(f"Loading existing courses from {COURSES_FILE}...")
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    print(f"Found {len(courses)} existing courses")
    print(f"Generating {len(IGOLF_COURSES)} igolf courses...")
    
    # Create igolf courses
    igolf_courses = []
    for i, course_data in enumerate(IGOLF_COURSES):
        igolf_course = create_igolf_course(course_data, i)
        igolf_courses.append(igolf_course)
        print(f"  Created: {igolf_course['name']} ({igolf_course['id']})")
    
    # Add to existing courses
    courses.extend(igolf_courses)
    
    print(f"\nSaving {len(courses)} total courses to {COURSES_FILE}...")
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Existing courses: {len(courses) - len(igolf_courses)}")
    print(f"  New igolf courses: {len(igolf_courses)}")
    print(f"  Total courses: {len(courses)}")
    print(f"\nIgolf courses are configured with:")
    print(f"  - isIgolf: true")
    print(f"  - hasImage: false (excluded from carousels and map)")
    print(f"  - Radar mapping (+/-5m accuracy)")
    print(f"  - Brief single-paragraph descriptions")

if __name__ == '__main__':
    main()

