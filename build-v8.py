#!/usr/bin/env python3
"""Build the cover-enabled index.html."""

# 43 cover IDs fetched from OpenLibrary
cover_ids = {
    0: 524560, 1: 1000639, 2: 12313764, 3: 524046, 4: 10526598,
    5: 10226552, 6: 8264706, 7: 1009216, 8: 7276258, 12: 9346537,
    14: 7355949, 16: 524402, 17: 10693768, 19: 524706, 20: 8598269,
    21: 6463375, 22: 8441703, 23: 8455453, 24: 9261466, 26: 8748478,
    27: 8759450, 31: 6979680, 36: 14621125, 40: 9157148, 45: 7314237,
    50: 8596360, 60: 8999878, 63: 14631258, 67: 10221348, 72: 9295719,
    77: 10226290, 82: 8665647, 86: 8576978, 91: 10282255, 96: 1286941,
    100: 10477770, 110: 3993167, 115: 4531927, 120: 8231823, 124: 10496793,
    128: 12375569, 132: 15138118, 136: 13518107,
}

with open('index.html', 'r') as f:
    content = f.read()

# Add cover image CSS
cover_css = """
.cover-img{width:50px;height:75px;border-radius:4px;object-fit:cover;flex-shrink:0;border:1px solid var(--border);opacity:.9;transition:opacity .3s}
.book-card:hover .cover-img{opacity:1}
.cover-wrap{display:flex;flex-direction:column;justify-content:center;margin-top:6px}
"""

# Insert before closing </style>
content = content.replace('</style>\n', cover_css + '\n</style>\n')

# Add coverMap after var books = [...]
# Find the line with "var STORAGE_KEY"
cover_map_lines = []
for idx, cover_id in sorted(cover_ids.items()):
    cover_map_lines.append(f'{idx}:{cover_id}')
cover_map_js = f'var coverMap={{{",".join(cover_map_lines)}}};'

content = content.replace('var STORAGE_KEY = ', cover_map_js + '\n\nvar STORAGE_KEY = ')

# Modify the render function to include cover images
old_render_line = "            '<div class=\"book-head\"><div>' +"
new_render_block = """            '<div class="book-head">' + getCoverWrap(i) + '<div>' +"""

content = content.replace(old_render_line, new_render_block)

# Add getCoverWrap function before renderList
get_cover_func = """// Cover image rendering
var coverCache = {};
try { var cc = localStorage.getItem('scifi_covers_v1'); if (cc) coverCache = JSON.parse(cc); } catch(e) {}
function getCoverWrap(idx) {
    var cid = coverMap[idx] || coverCache[idx];
    if (cid) {
        return '<div class="cover-wrap"><img class="cover-img" src="https://covers.openlibrary.org/b/id/' + cid + '-S.jpg" alt="" loading="lazy"></div>';
    }
    // Placeholder + lazy-load trigger
    return '<div class="cover-wrap"><div class="cover-placeholder cover-img" data-idx="' + idx + '" data-loaded="0">📖</div></div>';
}

"""

content = content.replace('function renderList()', get_cover_func + 'function renderList()')

# Add lazy loading at the end
lazy_js = """
// Lazy load missing covers in background
(function lazyLoadMissingCovers(){
    var toLoad = [];
    for (var i = 0; i < books.length; i++) {
        if (!coverMap[i] && !coverCache[i]) toLoad.push(i);
    }
    if (!toLoad.length) return;
    console.log('[covers] ' + toLoad.length + ' covers to lazy-load');
    
    var delay = 1500; // 1.5s between requests - polite to OpenLibrary
    var active = 0;
    var maxActive = 3; // 3 parallel streams
    
    function loadOne(idx) {
        var b = books[idx];
        fetch('https://openlibrary.org/search.json?title=' + encodeURIComponent(b.title) +
            '&author=' + encodeURIComponent(b.author.split(' + ')[0]) +
            '&limit=1&fields=cover_i')
            .then(r => r.json())
            .then(d => {
                if (d.docs && d.docs[0] && d.docs[0].cover_i) {
                    var cid = d.docs[0].cover_i;
                    coverCache[idx] = cid;
                    try { localStorage.setItem('scifi_covers_v1', JSON.stringify(coverCache)); } catch(e) {}
                    var placeholder = document.querySelector('.cover-placeholder[data-idx="' + idx + '"]');
                    if (placeholder) {
                        placeholder.outerHTML = '<img class="cover-img" src="https://covers.openlibrary.org/b/id/' + cid + '-S.jpg" alt="" loading="lazy">';
                    }
                    console.log('[covers] Found: ' + b.title + ' → #' + cid);
                }
            })
            .catch(function(e) { console.log('[covers] Failed: ' + b.title); })
            .then(function() { active--; runNext(); });
    }
    
    function runNext() {
        if (!toLoad.length || active >= maxActive) return;
        active++;
        loadOne(toLoad.shift());
        setTimeout(runNext, delay); // Rate limit
    }
    
    // Start 3 parallel
    for (var i = 0; i < maxActive; i++) runNext();
})();
"""

content = content.replace('</script>\n</body>', lazy_js + '\n</script>\n</body>')

with open('index.html', 'w') as f:
    f.write(content)

print(f'✅ index.html updated — v8 with cover images')
print(f'   Pre-baked covers: {len(cover_ids)}/140')
print(f'   Remaining: {140 - len(cover_ids)} (lazy-loaded in browser)')
