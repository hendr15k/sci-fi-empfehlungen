#!/usr/bin/env python3
"""Build the cover-enabled index.html with cover images."""

cover_map = {
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

# Read original
with open('index.html', 'r') as f:
    html = f.read()

# Add cover image CSS
cover_css = """
/* Cover Images */
.cover-wrap {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 56px;
  height: 84px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--input-bg);
  border: 1px solid var(--border);
}
.cover-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.cover-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4em;
  color: var(--text-muted);
  background: var(--input-bg);
}
.book-head {
  padding-left: 8px;
  position: relative;
}
.read-cb {
  transform: translateY(-2px);
}
</style>
"""

# Insert cover CSS before closing </style>
html = html.replace('</style>\n\n', cover_css + '\n')

# Add coverMap and lazyLoading JS before the existing coverMap if any, or after var books = [...]
cover_map_js = f'var coverMap = {json.dumps(cover_map)};\n// Lazy load remaining covers'

# Find where var books starts and coverMap should be added after it
html = html.replace('var STORAGE_KEY', cover_map_js + '\n\nvar STORAGE_KEY')

# Modify the render function to include cover images
old_render = """        grid.innerHTML += '<div class=\"' + cls + '\">' +
            '<div class=\"book-head\"><div>' +
            '<div class=\"book-title\">' +
            '<label class=\"read-cb\"><input type=\"checkbox\" ' + (r ? 'checked' : '') + ' onclick=\"toggleRead(' + i + ')\"><span class=\"cb-mark\"></span></label>' +
            b.title + badges + '</div>' +
            '<div class=\"book-meta\">' + b.author + ' (' + b.year + ')</div>' +
            '</div><div class=\"rating\">' + b.stars + '</div></div>' +
            '<span class=\"subgenre\">' + b.genre + '</span>' +
            '<div class=\"why\">' + b.why + '</div></div>';"""

new_render = """        var coverHtml = getCoverHtml(i);
        grid.innerHTML += '<div class=\"' + cls + '\">' +
            '<div class=\"book-head\">' + coverHtml + '<div>' +
            '<div class=\"book-title\">' +
            '<label class=\"read-cb\"><input type=\"checkbox\" ' + (r ? 'checked' : '') + ' onclick=\"toggleRead(' + i + ')\"><span class=\"cb-mark\"></span></label>' +
            b.title + badges + '</div>' +
            '<div class=\"book-meta\">' + b.author + ' (' + b.year + ')</div>' +
            '</div><div class=\"rating\">' + b.stars + '</div></div>' +
            '<span class=\"subgenre\">' + b.genre + '</span>' +
            '<div class=\"why\">' + b.why + '</div></div>';"""

html = html.replace(old_render, new_render)

# Add getCoverHtml function and lazy loading after the renderList function
lazy_load_js = """
// Cover image functions
function getCoverHtml(idx) {
    if (coverMap[idx]) {
        var img = 'https://covers.openlibrary.org/b/id/' + coverMap[idx] + '-S.jpg';
        return '<div class=\"cover-wrap\"><img src=\"' + img + '\" alt=\"Cover\" loading=\"lazy\"></div>';
    }
    return '<div class=\"cover-wrap\"><div class=\"cover-placeholder\" id=\"cover_' + idx + '\">📖</div></div>';
}

// Lazy load covers that aren't in the map yet
(function lazyLoadCovers() {
    var COVER_STORAGE = 'scifi_covers_v1';
    var coverCache = {};
    try { var c = localStorage.getItem(COVER_STORAGE); if (c) coverCache = JSON.parse(c); } catch(e) {}
    
    // Merge cached covers into coverMap
    for (var k in coverCache) {
        if (coverCache[k] && !coverMap[k]) {
            coverMap[k] = coverCache[k];
        }
    }
    
    function fetchCover(idx, cb) {
        fetch('https://covers.openlibrary.org/b/olid/default-' + idx + '-S.json')
            .then(r => {
                if (!r.ok) return cb(null);
                return r.json();
            })
            .then(d => cb(d && d.cover_id ? d.cover_id : null))
            .catch(() => cb(null));
    }
    
    // Batch lazy load with delay
    var pendingIdx = [];
    for (var i = 0; i < books.length; i++) {
        if (!coverMap[i]) pendingIdx.push(i);
    }
    
    if (pendingIdx.length === 0) return;
    
    var delay = 1200; // 1.2s between requests
    var loaded = 0;
    
    function nextCover() {
        if (pendingIdx.length === 0) return;
        var idx = pendingIdx.shift();
        var book = books[idx];
        
        var query = 'https://openlibrary.org/search.json?title=' + encodeURIComponent(book.title) + '&author=' + encodeURIComponent(book.author.split(' + ')[0]) + '&limit=1&fields=cover_i';
        
        setTimeout(function() {
            fetch(query)
                .then(r => r.json())
                .then(function(d) {
                    if (d.docs && d.docs[0] && d.docs[0].cover_i) {
                        coverMap[idx] = d.docs[0].cover_i;
                        coverCache[idx] = d.docs[0].cover_i;
                        try { localStorage.setItem(COVER_STORAGE, JSON.stringify(coverCache)); } catch(e) {}
                        // Update DOM if visible
                        var el = document.getElementById('cover_' + idx);
                        if (el) {
                            el.outerHTML = '<img src=\"https://covers.openlibrary.org/b/id/' + d.docs[0].cover_i + '-S.jpg\" alt=\"Cover\" style=\"width:100%;height:100%;object-fit:cover;display:block\">';
                        }
                        loaded++;
                    }
                })
                .catch(function() {})
                .then(function() { nextCover(); });
        }, delay);
    }
    
    // Start loading after page renders
    setTimeout(function() {
        for (var i = 0; i < 5; i++) nextCover(); // Start 5 parallel streams
    }, 500);
    
    console.log('[covers] 43 preloaded, ' + pendingIdx.length + ' remaining, lazy loading...');
})();
"""

html = html.replace('renderList();\nupdateProgress();', lazy_load_js + '\nrenderList();\nupdateProgress();')

# Update footer
html = html.replace('Reading Tracker: lokaler Browser-Speicher<br>', 
                   'Reading Tracker: lokaler Browser-Speicher<br>' +
                   'Cover-Bilder: Open Library <a href=\"https://openlibrary.org/dev/docs/api/covers\">Covers API</a><br>')

# Update meta
html = html.replace('var books = [', '// v8 - mit Cover-Bildern (OpenLibrary API)\nvar books = [')

with open('index.html', 'w') as f:
    f.write(html)

print(f'✅ index.html updated with cover images (43 preloaded covers + {sum(1 for k in cover_map if k is not None)} remaining lazy-load)')
