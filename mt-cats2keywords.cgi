#!/usr/bin/perl -w
#
# mt-cats2keywords.cgi: A simple tool for adding keywords to each entries based on their categories
# 
# Release 0.10 (Apr 18, 2005)
#
# This software is provided as-is. You may use it for commercial or 
# personal use. If you distribute it, please keep this notice intact.
#
# Copyright (c) 2005 Hirotaka Ogawa

# PLEASE CHANGE THIS "BLOG_ID" AS YOU WANT
use constant BLOG_ID => 1;

use strict;
local $|=1;

my($MT_DIR);
BEGIN {
    if ($0 =~ m!(.*[/\\])!) {
        $MT_DIR = $1;
    } else {
        $MT_DIR = './';
    }
    unshift @INC, $MT_DIR . 'lib';
    unshift @INC, $MT_DIR . 'extlib';
}

use MT;
use MT::Entry;
use MT::Category;

print "Content-Type: text/html\n\n";
print <<HTML;
<html>
<head><title>mt-cats2keywords</title></head>
<body>
<h1>mt-cats2keywords</h1>

<pre>
HTML

my $mt = MT->new;
my $e_iter = MT::Entry->load_iter({ blog_id => BLOG_ID });
while (my $e = $e_iter->()) {
    next if $e->keywords;
    my $cats = $e->categories;
    next unless $cats && @$cats;
    my $keywords = join ' ', map { $_->label } @$cats;
    $e->keywords($keywords);
    $e->save
	or printf ("[ERR] %s at MT::Entry->id: [%s]\n", $e->errstr, $e->id);
    printf("Entry [%s] title=%s keywords=%s\n", $e->id, $e->title, $e->keywords);
}

print <<HTML;
</pre>
<p><strong>Successfully added keywords.</strong></p>
</body>
</html>
HTML
