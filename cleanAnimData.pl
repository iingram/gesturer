#!/usr/bin/perl

# EXAMPLE USAGE: cat animData.fbx | ./cleanAnimData.pl "Cube" "R" "Y" "-50" "-1" > pitch.csv
# argv[1] = name of object as named in blender
# argv[2] = type of transformation
#           axis
#           offset (add to every rotation value)
#           multiplier (for reversing rotation if coordinate system is opp. of motors)
#           output     > pitch/yaw/roll.csv
#           

use strict;
use warnings;

my $divisor = 46001413368/1000;
my $fixed = 0;
my $zeroThreshhold = 0.00001;

my $queryModel = $ARGV[0];        #in this case: Cube, Camera, or Lamp
my $queryChannel = "Transform";   #not sure what other possibilities are - only Transform appears in .fbx
my $queryAnimType = $ARGV[1];     #(T)ranslate, (R)otate, (S)cale
my $queryAxis = $ARGV[2];         #X, Y, Z
my $offset = $ARGV[3];            #offset added to correct values (use 90 in this case, 0 if no offset needed)
my $multiplier = $ARGV[4];         #multiplier to account for "flipped" values -> either 1 or -1 (usually)

my $modelCheck = 0;
my $channelCheck = 0;
my $animTypeCheck = 0;
my $axisCheck = 0;

print "time,value\n";

while(<STDIN>){

  if(/^\s{2}Model: "Model::(.*)"/) {
    if($1 eq $queryModel) {
      $modelCheck = 1;
    } else {
      $modelCheck = 0;
    }
  }

  if(/^\s{3}Channel: "(.*)"/) {
    if($1 eq $queryChannel) {
      $channelCheck = 1;
    } else {
      $channelCheck = 0;
    }
  }
  elsif(/^\s{4}Channel: "(.*)"/) {
    if($1 eq $queryAnimType) {
      $animTypeCheck = 1;
    } else {
      $animTypeCheck = 0;
    }
  }
  elsif(/^\s{5}Channel: "(.*)"/) {
    if($1 eq $queryAxis) {
      $axisCheck = 1;
    } else {
      $axisCheck = 0;
    }
  }

    
  if(/^\s{7}(\d*),([-+]?[0-9]*\.[0-9]+),/){
	$fixed = $1/$divisor;
	$fixed = int($fixed);
	my $corrected = ($2+$offset) * $multiplier;
	#if corrected value is close enough to 0, round it to 0
	if (abs($corrected) < $zeroThreshhold) {
	  $corrected = 0;
	}

	if ($channelCheck && $modelCheck && $animTypeCheck && $axisCheck) {
	  print "$fixed,$corrected\n";
	}
  }
}
