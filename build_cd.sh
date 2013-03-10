#!/bin/sh

make clean
make html

sed -i '/jQuery(func{ Search.loadIndex("searchindex.js"); });/d' build/html/search.html
sed -i '/jQuery(function() { Search.loadIndex("searchindex.js"); });/d' build/html/search.html
sed -i 's/<\/head>/<script type="text\/javascript" src="searchindex.js"><\/script><\/head>/g' build/html/search.html

