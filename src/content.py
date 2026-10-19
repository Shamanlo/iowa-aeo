"""Site content: locations, industries, simulator questions and FAQs.

Edit this file to change copy. Run `python3 build.py` to regenerate docs/.
"""

# ---------------------------------------------------------------------------
# Locations: four hub metros, each with nearby towns.
# Blurbs stick to well-known, verifiable facts about each place.
# ---------------------------------------------------------------------------
HUBS = [
    {
        "slug": "des-moines",
        "name": "Des Moines",
        "query_city": "Des Moines",
        "region": "Central Iowa",
        "blurb": "Iowa's capital and largest metro. Des Moines businesses compete with "
                 "the busiest field of restaurants, contractors, clinics and firms in the state, "
                 "so AI assistants have plenty of names to choose between.",
        "towns": [
            ("West Des Moines", "west-des-moines", "IA", "Home to Valley Junction and the Jordan Creek area, West Des Moines is one of the metro's busiest places to shop, eat and do business."),
            ("Ankeny", "ankeny", "IA", "One of the fastest-growing cities in Iowa, Ankeny is full of new households searching for go-to restaurants, contractors and family services."),
            ("Urbandale", "urbandale", "IA", "A northwest-metro suburb and home of Living History Farms, Urbandale mixes long-time residents with growing commercial corridors."),
            ("Johnston", "johnston", "IA", "On the north side of the metro near Saylorville Lake, Johnston is a fast-growing suburb with a strong professional and family base."),
            ("Waukee", "waukee", "IA", "A fast-growing western suburb, Waukee families lean on quick answers to find dentists, contractors and places to eat nearby."),
            ("Clive", "clive", "IA", "A western suburb along the Clive Greenbelt Trail, Clive is packed with professional offices, clinics and local service businesses."),
            ("Altoona", "altoona", "IA", "East of Des Moines and home to Adventureland and Prairie Meadows, Altoona draws visitors who ask AI where to eat and stay."),
            ("Grimes", "grimes", "IA", "A growing northwest-metro community where new residents rely on search and AI to find trusted local services."),
            ("Norwalk", "norwalk", "IA", "Just south of Des Moines, Norwalk is a growing community where homeowners look for nearby contractors and family services."),
            ("Indianola", "indianola", "IA", "The Warren County seat and home of Simpson College, Indianola has a loyal local market and plenty of metro commuters."),
            ("Ames", "ames", "IA", "Home of Iowa State University, Ames has a constant flow of students, staff and families asking AI where to go."),
        ],
    },
    {
        "slug": "cedar-rapids",
        "name": "Cedar Rapids",
        "query_city": "Cedar Rapids",
        "region": "Eastern Iowa",
        "blurb": "Iowa's second-largest city and the anchor of the Corridor. Cedar Rapids "
                 "customers search across Marion, Hiawatha and the surrounding towns, so clean, "
                 "consistent business facts decide who AI recommends.",
        "towns": [
            ("Marion", "marion", "IA", "Cedar Rapids' neighbor to the northeast, Marion is a growing city with a busy uptown district and plenty of young families."),
            ("Hiawatha", "hiawatha", "IA", "On the north side of Cedar Rapids, Hiawatha has a strong mix of retail, industrial and service businesses."),
            ("Robins", "robins", "IA", "A small, fast-growing community north of Cedar Rapids where residents look to the whole metro for services."),
            ("Mount Vernon", "mount-vernon", "IA", "Home of Cornell College, Mount Vernon is a historic small town with a well-loved local dining and shopping scene."),
            ("Fairfax", "fairfax", "IA", "Southwest of Cedar Rapids, Fairfax is a growing small town where homeowners need nearby contractors and services."),
            ("Ely", "ely", "IA", "A small community between Cedar Rapids and Iowa City, where customers often ask AI who serves their area."),
        ],
    },
    {
        "slug": "iowa-city",
        "name": "Iowa City",
        "query_city": "Iowa City",
        "region": "Eastern Iowa",
        "blurb": "Home of the University of Iowa and a nationally known UNESCO City of Literature. "
                 "Students, faculty, patients and visitors all ask AI where to go, and new people "
                 "arrive every semester.",
        "towns": [
            ("Coralville", "coralville", "IA", "Home to the Iowa River Landing and Coral Ridge Mall, Coralville is a regional hub for dining, shopping and hotels."),
            ("North Liberty", "north-liberty", "IA", "One of the fastest-growing cities in Iowa, North Liberty has a steady stream of new residents looking for local services."),
            ("Tiffin", "tiffin", "IA", "A fast-growing town just west of Coralville where new homeowners search for nearby contractors and family services."),
            ("Solon", "solon", "IA", "A small town near Lake Macbride with a tight-knit local business community and plenty of Corridor commuters."),
            ("Kalona", "kalona", "IA", "Known for its Amish and Mennonite community, Kalona draws visitors searching for shops, bakeries and places to stay."),
            ("West Branch", "west-branch", "IA", "The birthplace of Herbert Hoover, West Branch is a historic small town that draws visitors and growing families."),
        ],
    },
    {
        "slug": "quad-cities",
        "name": "Quad Cities",
        "query_city": "Davenport",
        "region": "Eastern Iowa & Western Illinois",
        "blurb": "A two-state metro on the Mississippi River. Quad Cities customers cross the river "
                 "for restaurants, healthcare and services, so AI has to understand exactly where "
                 "you are and who you serve.",
        "towns": [
            ("Davenport", "davenport", "IA", "The largest city in the Quad Cities, Davenport has a riverfront downtown, the Village of East Davenport and a large local business market."),
            ("Bettendorf", "bettendorf", "IA", "A riverfront city east of Davenport with strong schools, growing neighborhoods and plenty of family-focused businesses."),
            ("LeClaire", "leclaire", "IA", "A historic Mississippi River town and Buffalo Bill Cody's birthplace, LeClaire draws visitors to its riverfront shops and restaurants."),
            ("Eldridge", "eldridge", "IA", "A growing community north of Davenport, home to many families who commute across the Quad Cities."),
            ("Blue Grass", "blue-grass", "IA", "A small town west of Davenport where residents rely on the wider metro for services and ask AI who covers their area."),
            ("Moline", "moline", "IL", "On the Illinois side of the river and home to John Deere's world headquarters, Moline has a busy downtown and riverfront."),
            ("Rock Island", "rock-island", "IL", "Home to the Rock Island Arsenal and Augustana College, Rock Island has a historic downtown and a strong local business community."),
            ("East Moline", "east-moline", "IL", "On the Illinois side along the Mississippi, East Moline is a growing riverfront community with a strong local base."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Industries. Each question template uses {city}. `you` is the placeholder
# business name shown in the simulator; `review`/`site` describe what the
# signals unlock in the AI's answer.
# ---------------------------------------------------------------------------
INDUSTRIES = [
    {
        "slug": "restaurants",
        "name": "Restaurants & Bars",
        "short": "Restaurants",
        "icon": "utensils",
        "lede": "When someone asks AI where to eat tonight, it names three or four places. We make sure yours is one of them.",
        "questions": [
            {"q": "What's a good restaurant in {city} for a birthday dinner for six people?", "you": "Your Restaurant",
             "review": "guests rave about birthday dinners and big tables", "site": "the menu, group seating and reservations are easy to find"},
            {"q": "Where can I get a great brunch in {city} this Sunday that takes reservations?", "you": "Your Restaurant",
             "review": "reviews mention the brunch menu by name", "site": "Sunday hours and how to book are spelled out"},
        ],
        "signals": [
            "Menus, hours and price range that match on Google, Apple Maps, Yelp and your website",
            "Reviews that mention specific dishes, occasions and group sizes",
            "Pages that answer “Do you take reservations?”, “Is there parking?” and “Can you host a party of 12?”",
            "Mentions in local “best of” lists, food blogs and event guides",
        ],
        "faq": [
            ("Can AEO help a restaurant get more reservations?", "AEO makes sure that when someone asks ChatGPT, Gemini or Google where to eat, your restaurant is clearly described and easy to recommend. That means accurate hours, menus and booking details, plus reviews and mentions that show what you're known for."),
            ("Does my menu need to be on my website as text?", "Yes. AI systems read text much more reliably than PDFs or photos of menus. A simple HTML menu page with dish names, dietary notes and prices gives AI something specific to quote."),
            ("What about seasonal hours and special events?", "We help you keep holiday hours, patio season and events consistent across your listings and site, so AI doesn't send people to a closed door."),
        ],
    },
    {
        "slug": "home-services",
        "name": "Home Services",
        "short": "Home Services",
        "icon": "wrench",
        "lede": "Plumbers, HVAC, roofers and electricians: when a pipe bursts, people ask AI who can come today.",
        "questions": [
            {"q": "My water heater is leaking. Is there a plumber in {city} who can come today?", "you": "Your Plumbing Co.",
             "review": "customers mention same-day water heater repairs", "site": "emergency hours and service area are listed clearly"},
            {"q": "Who's a reliable furnace repair company in {city} that does weekend calls?", "you": "Your HVAC Co.",
             "review": "reviews describe fast weekend furnace fixes", "site": "weekend availability and towns served are spelled out"},
            {"q": "Can you recommend a roofer in {city} for hail damage and insurance claims?", "you": "Your Roofing Co.",
             "review": "homeowners describe smooth hail damage claims", "site": "a clear page explains the insurance claim process"},
        ],
        "signals": [
            "A service-area list that names every town you actually cover",
            "Emergency and after-hours availability stated the same way everywhere",
            "Reviews that mention the job (“water heater”, “hail damage”, “AC repair”) and the town",
            "Licensing, insurance and warranty details AI can quote",
        ],
        "faq": [
            ("Why does AI recommend some contractors and not others?", "AI looks for a clear match between the request (“furnace repair in Ankeny this weekend”) and the facts it can find. Contractors with consistent listings, a named service area and reviews that describe the work get picked first."),
            ("Should I have a page for every town I serve?", "Pages for your main towns help, as long as each one is genuinely useful: the services you offer there, response times and local projects. Thin copy-and-paste pages don't help."),
            ("Does Google Business Profile still matter?", "Very much. Google AI Overviews and Gemini lean heavily on Google's own business data, and other assistants pull from Bing, Apple Maps and Yelp. We clean up all of them."),
        ],
    },
    {
        "slug": "dentists",
        "name": "Dentists & Orthodontists",
        "short": "Dentists",
        "icon": "tooth",
        "lede": "Patients ask AI for a dentist who takes their insurance and is gentle with nerves. Be the practice it names.",
        "questions": [
            {"q": "Can you recommend a dentist in {city} who's good with anxious patients and takes Delta Dental?", "you": "Your Dental Practice",
             "review": "patients say the team is gentle with nervous patients", "site": "accepted insurance plans are listed by name"},
            {"q": "Which dentist in {city} is good with young kids and takes new patients?", "you": "Your Dental Practice",
             "review": "parents mention how well the team handles kids", "site": "a new-patient page explains the first visit"},
        ],
        "signals": [
            "Accepted insurance plans listed by name on your site and listings",
            "Reviews that describe the experience: anxiety, kids, emergencies",
            "Service pages for implants, Invisalign, emergencies and pediatric care",
            "Provider bios with credentials and memberships AI can verify",
        ],
        "faq": [
            ("Do insurance details really affect AI answers?", "Yes. People ask “who takes Delta Dental” or “who accepts Wellmark” all the time. If your plans aren't written out clearly, AI can't confidently match you."),
            ("Is AEO HIPAA-safe?", "AEO works with public business information like services, insurance, hours and reviews. We never need patient records, and we'll help you respond to reviews without disclosing patient details."),
            ("How do we get more specific reviews?", "We set up a simple follow-up process that prompts patients to describe their visit in their own words, which gives AI far more to work with than a five-star rating alone."),
        ],
    },
    {
        "slug": "law-firms",
        "name": "Law Firms",
        "short": "Law Firms",
        "icon": "scale",
        "lede": "People ask AI which attorney fits their exact situation. Clear practice details make you the answer.",
        "questions": [
            {"q": "Who's a good estate planning attorney in {city} for a family farm and retirement accounts?", "you": "Your Law Firm",
             "review": "clients describe help planning a family farm transition", "site": "practice pages explain farm succession and trusts"},
            {"q": "I was rear-ended on I-80. Who's a good car accident lawyer in {city}?", "you": "Your Law Firm",
             "review": "clients describe being guided through an accident claim", "site": "a clear page covers what to do after a crash"},
        ],
        "signals": [
            "Practice-area pages that answer real client questions in plain English",
            "Attorney bios with bar admissions, education and focus areas",
            "Consistent firm name, address and phone across legal directories",
            "Mentions in local news, bar association and community sources",
        ],
        "faq": [
            ("Is AEO allowed under attorney advertising rules?", "AEO focuses on accurate, factual information about your firm: practice areas, attorneys, locations and client experiences. We avoid guarantees and outcome claims, and you approve all content."),
            ("Which directories matter most for law firms?", "Google, Bing and Apple Maps first, then the major legal directories and your state and local bar listings. AI cross-checks these, so consistency matters more than volume."),
            ("Can AI tell my practice areas apart?", "Only if you spell them out. A firm that lists “estate planning, farm succession and probate” on dedicated pages gets matched to far more questions than one with a single “Services” page."),
        ],
    },
    {
        "slug": "medical",
        "name": "Medical & Med Spas",
        "short": "Medical & Med Spas",
        "icon": "heart",
        "lede": "Clinics, chiropractors, physical therapists and med spas: AI is the new front desk for first-time patients.",
        "questions": [
            {"q": "Who's a good chiropractor in {city} for lower back pain who takes walk-ins?", "you": "Your Chiropractic",
             "review": "patients describe real relief for lower back pain", "site": "walk-in hours and insurance are listed clearly"},
            {"q": "Where can I get Botox in {city} from an experienced nurse injector?", "you": "Your Med Spa",
             "review": "clients mention natural-looking results by name", "site": "injector credentials and pricing are explained"},
        ],
        "signals": [
            "Provider credentials and specialties stated clearly",
            "Treatment pages that explain who it's for, what to expect and the cost",
            "Accurate hours, walk-in policy and insurance information",
            "Reviews that mention specific treatments and outcomes",
        ],
        "faq": [
            ("Will AI recommend a med spa or clinic it can't verify?", "It's far less likely to. AI favors providers whose credentials, services and location it can confirm across several trusted sources."),
            ("Do treatment prices need to be public?", "Not always, but clear starting prices or ranges help AI answer “how much does it cost” questions, and that's a big share of what people ask."),
            ("Is this compliant with healthcare marketing rules?", "We stick to factual, verifiable information and avoid outcome guarantees. You review and approve everything we publish."),
        ],
    },
    {
        "slug": "real-estate",
        "name": "Real Estate",
        "short": "Real Estate",
        "icon": "home",
        "lede": "Buyers and sellers ask AI which agent knows their neighborhood. Make sure it knows you.",
        "questions": [
            {"q": "Who's a good real estate agent in {city} for first-time home buyers?", "you": "Your Realty Team",
             "review": "first-time buyers describe being walked through every step", "site": "a buyer guide covers the neighborhoods you work"},
            {"q": "Which realtor in {city} should I call to sell my house fast?", "you": "Your Realty Team",
             "review": "sellers mention quick, smooth sales", "site": "recent sales and your process are laid out clearly"},
        ],
        "signals": [
            "Neighborhood and town pages written from real local knowledge",
            "Agent bios with license, brokerage and areas served",
            "Reviews that name the neighborhood and the type of deal",
            "Consistent profiles across Zillow, Realtor.com and Google",
        ],
        "faq": [
            ("Can an individual agent rank in AI answers, not just the brokerage?", "Yes. AI often names individual agents when their profile, reviews and content clearly connect them to a town and a type of client."),
            ("Do neighborhood guides help?", "Genuinely useful guides covering schools, commute, price ranges and what's nearby give AI something specific to quote when someone asks about that area."),
            ("Which profiles matter most?", "Google Business Profile, your brokerage profile, Zillow and Realtor.com. We make sure your name, photo, license and service area match everywhere."),
        ],
    },
    {
        "slug": "auto",
        "name": "Auto Repair & Dealers",
        "short": "Auto",
        "icon": "car",
        "lede": "“Who can fix my brakes today?” is a question AI answers every hour. Be the shop it trusts.",
        "questions": [
            {"q": "Is there an honest auto repair shop in {city} that can look at my brakes today?", "you": "Your Auto Shop",
             "review": "customers call the shop honest and fairly priced", "site": "same-day service and brake repair are explained"},
            {"q": "Where should I get new tires in {city} before winter?", "you": "Your Tire & Auto",
             "review": "reviews mention quick, fair tire installs", "site": "brands carried and winter tire options are listed"},
        ],
        "signals": [
            "Services, makes and models you work on, listed in plain text",
            "Hours, appointment and walk-in policy that match everywhere",
            "Reviews that mention honesty, pricing and the specific repair",
            "Certifications and warranties AI can verify",
        ],
        "faq": [
            ("Why does AI keep recommending chain shops?", "Chains usually have consistent listings and lots of structured data. A local shop with clean facts and specific reviews can absolutely compete, and often wins on trust."),
            ("Should I list the vehicle brands I service?", "Yes. “Who works on Subarus in Ames?” is a real question. If your site doesn't say it, AI can't answer it with your name."),
            ("Does AEO help dealerships too?", "Yes. Dealerships benefit from clear inventory, service department and financing pages, plus consistent location data for every rooftop."),
        ],
    },
    {
        "slug": "agriculture",
        "name": "Ag & Rural Businesses",
        "short": "Agriculture",
        "icon": "corn",
        "lede": "Seed dealers, ag equipment, large-animal vets and rural services: Iowa runs on agriculture, and farmers ask AI too.",
        "questions": [
            {"q": "Who's a good large-animal vet near {city} that does farm calls?", "you": "Your Vet Clinic",
             "review": "farmers mention fast, reliable farm calls", "site": "farm call coverage and emergency hours are listed"},
            {"q": "Where can I get my combine serviced near {city} before harvest?", "you": "Your Equipment Co.",
             "review": "customers describe quick turnaround before harvest", "site": "equipment brands and service area are spelled out"},
        ],
        "signals": [
            "A service radius that names the counties and towns you cover",
            "Equipment brands, seed lines and services listed in plain text",
            "Seasonal hours for planting and harvest that match everywhere",
            "Mentions from co-ops, extension resources and farm organizations",
        ],
        "faq": [
            ("Do farmers really use AI to find suppliers?", "More every season. Farmers use ChatGPT, Gemini and Google AI Overviews to compare options, check hours and find who services their equipment, often from the cab."),
            ("We're rural. Does location data matter?", "Even more. Rural addresses and service areas are often messy across map platforms. Getting them right is one of the fastest AEO wins for ag businesses."),
            ("Can you help with seasonal content?", "Yes. Planting, spraying and harvest-season pages answer the timely questions your customers are already asking."),
        ],
    },
]

# ---------------------------------------------------------------------------
# Services ("What we do" bento).
# ---------------------------------------------------------------------------
SERVICES = [
    {"title": "AI Visibility Audit", "icon": "search", "tone": "dark",
     "body": "We ask ChatGPT, Gemini, Perplexity, Claude and Google AI Overviews the questions your customers ask, then show you who gets named, how you're described, and why."},
    {"title": "Entity & Listing Cleanup", "icon": "list", "tone": "accent",
     "body": "AI pulls facts from Google, Bing, Apple Maps, Yelp and industry directories. We make your name, hours, services and details consistent everywhere it looks."},
    {"title": "Answer-Ready Content", "icon": "doc", "tone": "light",
     "body": "Service pages, FAQs and structured data that answer real customer questions in plain language, so AI has something specific to quote."},
    {"title": "Citations & Reviews", "icon": "link", "tone": "pale",
     "body": "Mentions in local press, guides and directories AI trusts, plus a review process that gets customers describing what you do best."},
]

PROCESS = [
    ("Audit", "We test dozens of real customer questions across five AI assistants and record exactly who gets recommended in your town."),
    ("Fix the facts", "We clean up your listings, website details and structured data so every source tells AI the same, accurate story."),
    ("Publish answers", "We build pages and FAQs that answer the exact questions people ask AI about your business and your town."),
    ("Earn trust & track", "We grow reviews and local mentions, then re-test every month so you can see your AI visibility change."),
]

SEO_VS_AEO = [
    ("Goal", "Rank in a list of ten blue links", "Get named in the answer itself"),
    ("Where it shows", "Google and Bing results pages", "ChatGPT, Gemini, Perplexity, Claude, Google AI Overviews"),
    ("What wins", "Keywords, backlinks, page speed", "Consistent facts, specific reviews, clear answers, trusted mentions"),
    ("How people search", "Short keywords: “plumber Ankeny”", "Full questions: “Who can fix my water heater in Ankeny today?”"),
    ("What you measure", "Rankings and clicks", "Mentions, recommendations and how AI describes you"),
]

HOME_FAQ = [
    ("What is Answer Engine Optimization (AEO)?",
     "AEO is the work of making your business easy for AI assistants to understand, trust and recommend. When someone asks ChatGPT, Gemini, Perplexity, Claude or Google AI Overviews for a local business, AEO helps make sure your business is in the answer, and described accurately."),
    ("How is AEO different from SEO?",
     "SEO helps you rank in a list of search results. AEO helps you get named in a single AI-written answer. They overlap, since both need a good website and accurate listings, but AEO puts extra weight on consistent facts, specific reviews, plain-language answers and third-party mentions."),
    ("Which AI tools does AEO help with?",
     "The work we do helps across ChatGPT, Google Gemini, Google AI Overviews and AI Mode, Perplexity, Claude and Microsoft Copilot. They all read the open web and major listing sources, so clean, consistent information helps everywhere."),
    ("How long does it take to show up in AI answers?",
     "Listing and website fixes are often picked up within a few weeks. Reviews, content and third-party mentions build over a few months. Every AI updates on its own schedule, so we re-test monthly and show you what's changed."),
    ("Do I still need SEO?",
     "Yes. Google search still matters, and much of what AI reads comes from pages that rank well. Good AEO and good SEO support each other, and we build with both in mind."),
    ("Do you only work in Des Moines, Cedar Rapids, Iowa City and the Quad Cities?",
     "Those are our home markets, but we work with businesses anywhere in Iowa and across the river in Illinois. AEO is mostly done online, and we're happy to meet in person around the state."),
    ("What does the free AI visibility check include?",
     "We ask the major AI assistants a handful of the questions your customers would ask, and send you what they say: whether you're mentioned, who's recommended instead, and the top fixes we'd make first."),
]
