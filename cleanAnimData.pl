#!/usr/bin/perl
use strict;
use warnings;

my $last1 = 1000000000000000000;
my $last2 = 42;
my $divisor = 46001413368/1000;
my $fixed = 0;

print "time,value\n";

while(<STDIN>){
#    print "$1,$2\n" if /^\s{7}(\d*),([-+]?[0-9]*\.[0-9]+),/;
    
    if(/^\s{7}(\d*),([-+]?[0-9]*\.[0-9]+),/){
# this will cut off the very last entry but I am going to consider that fine for now
	$fixed = $last1/$divisor;
	$fixed = int($fixed);
 	print "$fixed,$last2\n" if $last1 < $1;
 	
 	$last1 = $1;
 	$last2 = $2+90;  #this adjusts for an offset that comes out of blender (at least on the rotation I am using)
    }
}
