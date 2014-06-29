#!/usr/bin/perl
use strict;
use warnings;

my $last1 = 1000000000000000000;
my $last2 = 42;
my $divisor = 46001413368/1000;
my $fixed = 0;


while(<STDIN>){

  if(/^\s{2}Model: "Model::(.*)"/) {
    print "\nMODEL: $1\n";
  }

  if(/^\s{3}Channel: "(.*)"/) {
    print "\nchannel: $1\n";
  }
  elsif(/^\s{4}Channel: "(.*)"/) {
    print "\nanimation type: ";
    if($1 eq 'T') {
      print "TRANSLATE";
    } elsif($1 eq 'R') {
      print "ROTATE";
    } elsif($1 eq 'S') {
      print "SCALE";
    }
    print "\n";
  }
  elsif(/^\s{5}Channel: "(.*)"/) {
    print "\naxis: $1\n";
  }

  if(/^\s{7}(\d*),([-+]?[0-9]*\.[0-9]+),/){
	$fixed = $last1/$divisor;
	$fixed = int($fixed);
 	print "$1,$2\n";
 	
 	$last1 = $1;
 	$last2 = $2;  
  }
}

