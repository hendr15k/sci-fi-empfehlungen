#!/usr/bin/env python3
"""Fetch cover IDs from OpenLibrary for all books - parallel version."""
import urllib.request
import json
import time
import concurrent.futures

books = [
    {"title":"Blindsight","author":"Peter Watts"},
    {"title":"Permutation City","author":"Greg Egan"},
    {"title":"Solaris","author":"Stanislaw Lem"},
    {"title":"Story of Your Life","author":"Ted Chiang"},
    {"title":"The Three-Body Problem","author":"Cixin Liu"},
    {"title":"Vita Nostra","author":"Marina Dyachenko"},
    {"title":"Children of Time","author":"Adrian Tchaikovsky"},
    {"title":"Diaspora","author":"Greg Egan"},
    {"title":"Embassytown","author":"China Mieville"},
    {"title":"Pushing Ice","author":"Alastair Reynolds"},
    {"title":"Schilder's Ladder","author":"Greg Egan"},
    {"title":"Neuromancer","author":"William Gibson"},
    {"title":"The Martian Chronicles","author":"Ray Bradbury"},
    {"title":"Accelerando","author":"Charles Stross"},
    {"title":"Ancillary Justice","author":"Ann Leckie"},
    {"title":"Snow Crash","author":"Neal Stephenson"},
    {"title":"Old Man's War","author":"John Scalzi"},
    {"title":"The Forever War","author":"Joe Haldeman"},
    {"title":"Down and Out in the Magic Kingdom","author":"Cory Doctorow"},
    {"title":"The Ghost Brigades","author":"John Scalzi"},
    {"title":"The Diamond Age","author":"Neal Stephenson"},
    {"title":"The Windup Girl","author":"Paolo Bacigalupi"},
    {"title":"Binti","author":"Nnedi Okorafor"},
    {"title":"The City & The City","author":"China Mieville"},
    {"title":"A Fire Upon the Deep","author":"Vernor Vinge"},
    {"title":"The Gone World","author":"Tom Sweterlitsch"},
    {"title":"Recursion","author":"Blake Crouch"},
    {"title":"The Warehouse","author":"Rob Hart"},
    {"title":"Ender's Game","author":"Orson Scott Card"},
    {"title":"Speaker for the Dead","author":"Orson Scott Card"},
    {"title":"The Left Hand of Darkness","author":"Ursula K. Le Guin"},
    {"title":"The Dispossessed","author":"Ursula K. Le Guin"},
    {"title":"Dune","author":"Frank Herbert"},
    {"title":"The Tainted Cup","author":"Robert Jackson Bennett"},
    {"title":"Someone You Can Build a Nest In","author":"John Wiswell"},
    {"title":"System Collapse","author":"Martha Wells"},
    {"title":"The Ministry of Time","author":"Kaliane Bradley"},
    {"title":"The Mercy of Gods","author":"James S.A. Corey"},
    {"title":"Annie Bot","author":"Sierra Greer"},
    {"title":"Orbital","author":"Samantha Harvey"},
    {"title":"All Systems Red","author":"Martha Wells"},
    {"title":"The Dark Forest","author":"Cixin Liu"},
    {"title":"Death's End","author":"Cixin Liu"},
    {"title":"The Player of Games","author":"Iain M. Banks"},
    {"title":"Use of Weapons","author":"Iain M. Banks"},
    {"title":"Leviathan Wakes","author":"James S.A. Corey"},
    {"title":"The Family Experiment","author":"David Nickell"},
    {"title":"Persepolis Rising","author":"James S.A. Corey"},
    {"title":"Leviathan Falls","author":"James S.A. Corey"},
    {"title":"Die Haarteppichknuepfer","author":"Andreas Eschbach"},
    {"title":"QualityLand","author":"Marc-Uwe Kling"},
    {"title":"QualityLand 2.0","author":"Marc-Uwe Kling"},
    {"title":"Herr aller Dinge","author":"Andreas Eschbach"},
    {"title":"Rakesfall","author":"Vajra Chandrasekera"},
    {"title":"Asunder","author":"Kerstin Hall"},
    {"title":"The Stardust Grail","author":"Sam Gaynor"},
    {"title":"Foundation","author":"Isaac Asimov"},
    {"title":"Children of Ruin","author":"Adrian Tchaikovsky"},
    {"title":"Consider Phlebas","author":"Iain M. Banks"},
    {"title":"Hyperion","author":"Dan Simmons"},
    {"title":"Ringworld","author":"Larry Niven"},
    {"title":"Gateway","author":"Frederik Pohl"},
    {"title":"Rendezvous with Rama","author":"Arthur C. Clarke"},
    {"title":"The Moon Is a Harsh Mistress","author":"Robert A. Heinlein"},
    {"title":"Flowers for Algernon","author":"Daniel Keyes"},
    {"title":"The Stars My Destination","author":"Alfred Bester"},
    {"title":"Childhood's End","author":"Arthur C. Clarke"},
    {"title":"A Canticle for Leibowitz","author":"Walter M. Miller Jr."},
    {"title":"Roadside Picnic","author":"Arkady Strugatsky"},
    {"title":"Blind Lake","author":"Robert Charles Wilson"},
    {"title":"Spin","author":"Robert Charles Wilson"},
    {"title":"Anathem","author":"Neal Stephenson"},
    {"title":"Seveneves","author":"Neal Stephenson"},
    {"title":"Dark Matter","author":"Blake Crouch"},
    {"title":"The Fifth Season","author":"N.K. Jemisin"},
    {"title":"The Obelisk Gate","author":"N.K. Jemisin"},
    {"title":"The Stone Sky","author":"N.K. Jemisin"},
    {"title":"Piranesi","author":"Susanna Clarke"},
    {"title":"The Kaiju Preservation Society","author":"John Scalzi"},
    {"title":"Project Hail Mary","author":"Andy Weir"},
    {"title":"Station Eleven","author":"Emily St. John Mandel"},
    {"title":"The Long Way to a Small, Angry Planet","author":"Becky Chambers"},
    {"title":"This Is How You Lose the Time War","author":"Amal El-Mohtar"},
    {"title":"The Locked Tomb: Gideon the Ninth","author":"Tamsyn Muir"},
    {"title":"Klara and the Sun","author":"Kazuo Ishiguro"},
    {"title":"Sea of Rust","author":"C. Robert Cargill"},
    {"title":"The Quantum Thief","author":"Hannu Rajaniemi"},
    {"title":"Red Mars","author":"Kim Stanley Robinson"},
    {"title":"The Space Merchants","author":"Frederik Pohl"},
    {"title":"We","author":"Yevgeny Zamyatin"},
    {"title":"The City We Became","author":"N.K. Jemisin"},
    {"title":"Axiom's End","author":"Lindsay Ellis"},
    {"title":"A Memory Called Empire","author":"Arkady Martine"},
    {"title":"Network Effect","author":"Martha Wells"},
    {"title":"Excession","author":"Iain M. Banks"},
    {"title":"Look to Windward","author":"Iain M. Banks"},
    {"title":"The Prefect","author":"Alastair Reynolds"},
    {"title":"Children of Angels","author":"Adrian Tchaikovsky"},
    {"title":"A Psalm for the Wild-Built","author":"Becky Chambers"},
    {"title":"A Prayer for the Crown-Shy","author":"Becky Chambers"},
    {"title":"The Ministry for the Future","author":"Kim Stanley Robinson"},
    {"title":"New York 2140","author":"Kim Stanley Robinson"},
    {"title":"Walkaway","author":"Cory Doctorow"},
    {"title":"Kafka on the Shore","author":"Haruki Murakami"},
    {"title":"Hard-Boiled Wonderland and the End of the World","author":"Haruki Murakami"},
    {"title":"Genocidal Organ","author":"Project Itoh"},
    {"title":"Harmony","author":"Project Itoh"},
    {"title":"The Empire of the Ants","author":"Bernard Werber"},
    {"title":"Exhalation","author":"Ted Chiang"},
    {"title":"Stories of Your Life and Others","author":"Ted Chiang"},
    {"title":"The Ones Who Walk Away from Omelas","author":"Ursula K. Le Guin"},
    {"title":"Nightfall","author":"Isaac Asimov"},
    {"title":"I Have No Mouth, and I Must Scream","author":"Harlan Ellison"},
    {"title":"The Last Question","author":"Isaac Asimov"},
    {"title":"The Nine Billion Names of God","author":"Arthur C. Clarke"},
    {"title":"Bloodchild","author":"Octavia E. Butler"},
    {"title":"The Paper Menagerie","author":"Ken Liu"},
    {"title":"Folding Beijing","author":"Hao Jingfang"},
    {"title":"Slaughterhouse-Five","author":"Kurt Vonnegut"},
    {"title":"Cat's Cradle","author":"Kurt Vonnegut"},
    {"title":"Brave New World","author":"Aldous Huxley"},
    {"title":"Fahrenheit 451","author":"Ray Bradbury"},
    {"title":"The Handmaid's Tale","author":"Margaret Atwood"},
    {"title":"Caliban's War","author":"James S.A. Corey"},
    {"title":"The Traitor Baru Cormorant","author":"Seth Dickinson"},
    {"title":"The Calculating Stars","author":"Mary Robinette Kowal"},
    {"title":"Light From Uncommon Stars","author":"Ryka Aoki"},
    {"title":"The Space Between Worlds","author":"Micaiah Johnson"},
    {"title":"Babel-17","author":"Samuel R. Delany"},
    {"title":"Tau Zero","author":"Poul Anderson"},
    {"title":"A Deepness in the Sky","author":"Vernor Vinge"},
    {"title":"Dragon's Egg","author":"Robert L. Forward"},
    {"title":"The Gods Themselves","author":"Isaac Asimov"},
    {"title":"The Word for World Is Forest","author":"Ursula K. Le Guin"},
    {"title":"The Lathe of Heaven","author":"Ursula K. Le Guin"},
    {"title":"City","author":"Clifford D. Simak"},
    {"title":"More Than Human","author":"Theodore Sturgeon"},
    {"title":"Dhalgren","author":"Samuel R. Delany"},
    {"title":"Nova","author":"Samuel R. Delany"},
    {"title":"The Iron Dream","author":"Norman Spinrad"},
]

def fetch_cover(idx, book):
    title = book['title']
    author = book['author']
    try:
        url = f'https://openlibrary.org/search.json?title={urllib.request.quote(title)}&author={urllib.request.quote(author.split(" + ")[0])}&limit=1'
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'SciFiSite/1.0')
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.loads(resp.read().decode())
        
        cover_id = None
        if data.get('docs') and len(data['docs']) > 0:
            doc = data['docs'][0]
            if doc.get('cover_i'):
                cover_id = doc['cover_i']
        
        return (idx, title, cover_id)
    except Exception as e:
        return (idx, title, None, str(e))

# Use 20 concurrent workers
cover_map = {}
errors = []

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_cover, idx, book): idx for idx, book in enumerate(books)}
    
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        idx = result[0]
        title = result[1]
        cover_id = result[2]
        
        cover_map[idx] = cover_id
        
        if cover_id is not None:
            print(f'{idx:3d}: {title} → cover_{cover_id}')
        elif len(result) > 3:
            print(f'{idx:3d}: {title} → ERROR: {result[3]}')
            errors.append(result)
        else:
            print(f'{idx:3d}: {title} → no cover')

print(f'\n=== Results ===')
print(f'Total: {len(books)}')
print(f'With covers: {sum(1 for v in cover_map.values() if v is not None)}')
print(f'Without covers: {sum(1 for v in cover_map.values() if v is None)}')

# Output as JavaScript
print(f'\n=== JavaScript coverMap ===')
print('var coverMap = {')
for idx in sorted(cover_map.keys()):
    if cover_map[idx] is not None:
        print(f'  {idx}: {cover_map[idx]},')
print('};')
