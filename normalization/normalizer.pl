#!/usr/bin/perl

#!/usr/bin/perl -n
use Encode;
use strict;
#use utf8;
use POSIX qw(locale_h);
use encoding 'utf8';

# command line processing
use Getopt::Long;

#use charnames "greek";

#use encoding qw[ utf8 ];

my $g_no_line_seg = 0;

my $ret = Getopt::Long::GetOptions("no-line-seg" => \$g_no_line_seg);

if ($ret == 0) {
warn("Error: usage is \"perl normalizer.pl [--no-line-seg] <language> <input_file>\n\".");
exit;
}


my $lang = shift(@ARGV);
my $text_fn = shift(@ARGV);
my $output = "";

sub num2power3str {
	my $p = shift;
	my $plural = shift;
	my %p3str;
	if ($plural == 0) {
	$p3str{"FRENCH"} = ["mille", "million", "milliard"];
	$p3str{"ENGLISH"} = ["thousand", "million", "billion"];
	$p3str{"ITALIAN"} = ["mille", "milione", "miliardo"];
	$p3str{"SPANISH"} = ["mil", "millón", "mil millones"];
	$p3str{"GERMAN"} = ["Tausend", "Million", "Milliarde"];
	}
	else {
	$p3str{"FRENCH"} = ["mille", "millions", "milliards"];
	$p3str{"ENGLISH"} = ["thousand", "million", "billion"];
	$p3str{"ITALIAN"} = ["mila", "milioni", "miliardi"];
	$p3str{"SPANISH"} = ["mil", "millones", "mil millones"];
	$p3str{"GERMAN"} = ["Tausend", "Millionen", "Milliarden"];	
	}
	return $p3str{$lang}[$p-1];
}


sub num2unitstr {
	my $n = shift;
	my $c = shift;
	my $d = shift;
	my $u = shift;
	my %unitstr;
	
	$unitstr{"FRENCH"} = {
	0 => "zéro",
	1 => "un",
	2 => "deux",
	3 => "trois",
	4 => "quatre",
	5 => "cinq",
	6 => "six",
	7 => "sept",
	8 => "huit",
	9 => "neuf",
	10 => "dix",
	11 => "onze",
	12 => "douze",
	13 => "treize",
	14 => "quatorze",
	15 => "quinze",
	16 => "seize",
	17 => "dix sept",
	18 => "dix huit",
	19 => "dix neuf",
	20 => "vingt",
	21 => "vingt et un",
	30 => "trente",
	31 => "tente et un",
	40 => "quarante",
	41 => "quarante et un",
	50 => "cinquante",
	51 => "cinquante et un",
	60 => "soixante",
	61 => "soixante et un",
	70 => "soixante dix",
	71 => "soixante et onze",
	72 => "soixante douze",
	73 => "soixante treize",
	74 => "soixante quatorze",
	75 => "soixante quinze",
	76 => "soixante seize",
	80 => "quatre vingt",
	90 => "quatre vingt dix",
	91 => "quatre vingt onze",
	92 => "quatre vingt douze",
	93 => "quatre vingt treize",
	94 => "quatre vingt quatorze",
	95 => "quatre vingt quinze",
	96 => "quatre vingt seize",
	100 => "cent"
	};
	
	$unitstr{"ITALIAN"} = {
	0 => "zero",
	1 => "uno",
	2 => "due",
	3 => "tre",
	4 => "quattro",
	5 => "cinque",
	6 => "sei",
	7 => "sette",
	8 => "otto",
	9 => "nove",
	10 => "dieci",
	11 => "undici",
	12 => "dodici",
	13 => "tredici",
	14 => "quattordici",
	15 => "quindici",
	16 => "sedici",
	17 => "diciassette",
	18 => "diciotto",
	19 => "diciannove",
	20 => "venti",
	21 => "ventuno",
	30 => "trenta",
	31 => "trentuno",
	38 => "tentrotto",
	40 => "quaranta",
	41 => "quarantuno",
	48 => "quarantotto",
	50 => "cinquanta",
	51 => "cinquantuno",
	58 => "cinquantotto",
	60 => "sessanta",
	61 => "sessantuno",
	68 => "sessantotto",
	70 => "settanta",
	71 => "settantuno",
	78 => "settantotto",
	80 => "ottanta",
	81 => "ottantuno",
	88 => "ottantotto",
	90 => "novanta",
	91 => "novantuno",
	98 => "novantotto",
	100 => "cento"
	};
	
	
	$unitstr{"ENGLISH"} = {
	0 => "zero",
	1 => "one",
	2 => "two",
	3 => "three",
	4 => "four",
	5 => "five",
	6 => "six",
	7 => "seven",
	8 => "eight",
	9 => "nine",
	10 => "ten",
	11 => "eleven",
	12 => "twelve",
	13 => "thirteen",
	14 => "fourteen",
	15 => "fifteen",
	16 => "sixteen",
	17 => "seventeen",
	18 => "eighteen",
	19 => "nineteen",
	20 => "twenty",
	30 => "thirty",
	40 => "forty",
	50 => "fifty",
	60 => "sixty",
	70 => "seventy",
	80 => "eighty",
	90 => "ninety",
	100 => "hundred"
	};
	
	
	$unitstr{"GERMAN"} = {
	0 => "null",
	1 => "ein",
	2 => "zwei",
	3 => "drei",
	4 => "vier",
	5 => "fünf",
	6 => "sechs",
	7 => "sieben",
	8 => "acht",
	9 => "neun",
	10 => "zehn",
	11 => "elf",
	12 => "zwölf",
	13 => "dreizhen",
	14 => "vierzehn",
	15 => "fünfzehn",
	16 => "sechzehn",
	17 => "siebzehn",
	18 => "achtzehn",
	19 => "neunzehn",
	20 => "zwanzig",
	21 => "ein und zwanzig",
	22 => "zwei und zwanzig",
	23 => "drei und zwanzig",
	24 => "vier und zwanzig",
	25 => "fünf und zwanzig",
	26 => "sechs und zwanzig",
	27 => "sieben und zwanzig",
	28 => "acht und zwanzig",
	29 => "neun und zwanzig",
	30 => "dreißig",
	31 => "ein und dreißig",
	32 => "zwei und dreißig",
	33 => "drei und dreißig",
	34 => "vier und dreißig",
	35 => "fünf und dreißig",
	36 => "sechs und dreißig",
	37 => "sieben und dreißig",
	38 => "acht und dreißig",
	39 => "neun und dreißig",
	40 => "vierzig",
	41 => "ein und vierzig",
	42 => "zwei und vierzig",
	43 => "drei und vierzig",
	44 => "vier und vierzig",
	45 => "fünf und vierzig",
	46 => "sechs und vierzig",
	47 => "sieben und vierzig",
	48 => "acht und vierzig",
	49 => "neun und vierzig",
	50 => "fünfzig",
	51 => "ein und fünfzig",
	52 => "zwei und fünfzig",
	53 => "drei und fünfzig",
	54 => "vier und fünfzig",
	55 => "fünf und fünfzig",
	56 => "sechs und fünfzig",
	57 => "sieben und fünfzig",
	58 => "acht und fünfzig",
	59 => "neun und fünfzig",
	60 => "sechzig",
	61 => "ein und sechzig",
	62 => "zwei und sechzig",
	63 => "drei und sechzig",
	64 => "vier und sechzig",
	65 => "fünf und sechzig",
	66 => "sechs und sechzig",
	67 => "sieben und sechzig",
	68 => "acht und sechzig",
	69 => "neun und sechzig",
	70 => "siebzig",
	71 => "ein und siebzig",
	72 => "zwei und siebzig",
	73 => "drei und siebzig",
	74 => "vier und siebzig",
	75 => "fünf und siebzig",
	76 => "sechs und siebzig",
	77 => "sieben und siebzig",
	78 => "acht und siebzig",
	79 => "neun und siebzig",
	80 => "achtzig",
	81 => "ein und achtzig",
	82 => "zwei und achtzig",
	83 => "drei und achtzig",
	84 => "vier und achtzig",
	85 => "fünf und achtzig",
	86 => "sechs und achtzig",
	87 => "sieben und achtzig",
	88 => "acht und achtzig",
	89 => "neun und achtzig",
	90 => "neunzig",
	91 => "ein und neunzig",
	92 => "zwei und neunzig",
	93 => "drei und neunzig",
	94 => "vier und neunzig",
	95 => "fünf und neunzig",
	96 => "sechs und neunzig",
	97 => "sieben und neunzig",
	98 => "acht und neunzig",
	99 => "neun und neunzig",
	100 => "hundert"
	};
	
	$unitstr{"SPANISH"} = {
	0 => "cero",
	1 => "uno",
	2 => "dos",
	3 => "tres",
	4 => "cuatro",
	5 => "cinco",
	6 => "seis",
	7 => "siete",
	8 => "ocho",
	9 => "nueve",
	10 => "diez",
	11 => "once",
	12 => "doce",
	13 => "trece",
	14 => "cartorce",
	15 => "quince",
	16 => "dieci séis",
	17 => "dieci siete",
	18 => "dieci ocho",
	19 => "dieci nueve",
	20 => "veinte",
	21 => "veinti uno",
	22 => "veinti dos",
	23 => "veinti tres",
	24 => "veinti cuatro",
	25 => "veinti cinco",
	26 => "veinti seis",
	27 => "veinti siete",
	28 => "veinti ocho",
	29 => "veinti nueve",
	30 => "treinta",
	31 => "treinta y uno",
	32 => "treinta y dos",
	33 => "treinta y tres",
	34 => "treinta y cuatro",
	35 => "treinta y cinco",
	36 => "treinta y seis",
	37 => "treinta y siete",
	38 => "treinta y ocho",
	39 => "treinta y nueve",
	40 => "cuarenta",
	41 => "cuarenta y uno",
	42 => "cuarenta y dos",
	43 => "cuarenta y tres",
	44 => "cuarenta y cuatro",
	45 => "cuarenta y cinco",
	46 => "cuarenta y seis",
	47 => "cuarenta y siete",
	48 => "cuarenta y ocho",
	49 => "cuarenta y nueve",
	50 => "cinquenta",
	51 => "cinquenta y uno",
	52 => "cinquenta y dos",
	53 => "cinquenta y tres",
	54 => "cinquenta y cuatro",
	55 => "cinquenta y cinco",
	56 => "cinquenta y seis",
	57 => "cinquenta y siete",
	58 => "cinquenta y ocho",
	59 => "cinquenta y nueve",
	60 => "sesenta",
	61 => "sesenta y uno",
	62 => "sesenta y dos",
	63 => "sesenta y tres",
	64 => "sesenta y cuatro",
	65 => "sesenta y cinco",
	66 => "sesenta y seis",
	67 => "sesenta y siete",
	68 => "sesenta y ocho",
	69 => "sesenta y nueve",
	70 => "setenta",
	71 => "setenta y uno",
	72 => "setenta y dos",
	73 => "setenta y tres",
	74 => "setenta y cuatro",
	75 => "setenta y cinco",
	76 => "setenta y seis",
	77 => "setenta y siete",
	78 => "setenta y ocho",
	79 => "setenta y nueve",
	80 => "ochenta",
	81 => "ochenta y uno",
	82 => "ochenta y dos",
	83 => "ochenta y tres",
	84 => "ochenta y cuatro",
	85 => "ochenta y cinco",
	86 => "ochenta y seis",
	87 => "ochenta y siete",
	88 => "ochenta y ocho",
	89 => "ochenta y nueve",
	90 => "noventa",
	91 => "noventa y uno",
	92 => "noventa y dos",
	93 => "noventa y tres",
	94 => "noventa y cuatro",
	95 => "noventa y cinco",
	96 => "noventa y seis",
	97 => "noventa y siete",
	98 => "noventa y ocho",
	99 => "noventa y nueve",
	100 => "cien",
	200 => "dos cientos",
	300 => "tres cientos",
	400 => "cuatro cientos",
	500 => "quinientos",
	600 => "seis cientos",
	700 => "sete cientos",
	800 => "ocho cientos",
	900 => "nove cientos"
	};
	
	
	#if N is special
	if (defined($unitstr{$lang}{$n})) {
		return $unitstr{$lang}{$n};
	}
	
	#otherwise
	my @output = ();
	if ($c > 1 && defined($unitstr{$lang}{$c*100})) {
		push(@output, $unitstr{$lang}{$c*100});	
	}
	elsif ($c > 1) {
		push(@output, $unitstr{$lang}{$c}, $unitstr{$lang}{100});
	}
	elsif ($c == 1) {
		push(@output, $unitstr{$lang}{100});
	}
	
	# 2 digits
	if (defined($unitstr{$lang}{$d*10+$u})) {
		push(@output,$unitstr{$lang}{$d*10+$u});
	}
	elsif ($d > 1 && defined($unitstr{$lang}{$d*10})) {
		push(@output,$unitstr{$lang}{$d*10}, $unitstr{$lang}{$u});
	}
	else {
		push(@output,$unitstr{$lang}{$u});
	}
	
	return join(" ", @output);
}

sub num2str {
	my $n = shift;
	my $m = $n;
	my $power3 = 0;
	my @output = "";
	my %point = (
	"FRENCH" => "virgule",
	"ENGLISH" => "point",
	"GERMAN" => "punkt",
	"ITALIAN" => "punti",
	"SPANISH" => "punto"
	);

	if ($n =~ /^([0-9]+)[,\.]([0-9]+)$/) {
		return num2str($1)." ".$point{$lang}." ".num2str($2);
	}
	while ($n =~ s/(\d{1,3})$//) {
		my $triple = $1;
		my ($c, $d, $u) = (int($triple/100), int($triple/10)%10, $triple%10);
		if ($triple > 0 && $power3 > 0) {
			my $plural = 0;
			if ($triple > 1) { $plural = 1; }
			unshift(@output, num2power3str($power3,$plural));
		}
		if ($triple != 0 || $power3 > 0) {
		unshift(@output, "= ".num2unitstr($triple, $c, $d, $u));
		}
		$power3++;
	}
#	my $res = "$m = ".join(" ", @output);
	my $res = join(" ", @output);
	
	#specificities
	$res =~ s/= un mille/= mille/;
	
	$res =~ s/ ?= ?/ /;
	return $res;
}


sub abbrev {
	my $text = shift;
	my %ab = ();
	$ab{'ENGLISH'} = {
		            'Mr\.' => 'Mister',
		            'Mrs\.' => 'Misses',
		            'Ms\.' => 'Miss',
		            'Dr\.' => 'Doctor',
		            'Prof\.' => 'Professor',
		            'etc\.' => 'et cetera .',
		            '%' => 'per cent'
		            };
	$ab{'SPANISH'} = {
		            'Sr\.' => 'Señor',
		            'Sra\.' => 'Señora',
		            'Srta\.' => 'Señorita',
		            'Dr\.' => 'Doctor',
		            'Dra\.' => 'Doctora',
		            'Prof\.' => 'Profesor',
		            'Profa\.' => 'Profesora',
		            'etc\.' => 'et cetera .',
		            '%' => 'por ciento'
		            };
	$ab{'ITALIAN'} = {
		            'Sig\.' => 'Signore',
		            'Sig\.ra' => 'Signora',
		            'Sig\.na' => 'Signorina',
		            'Dr\.' => 'Dottore',
		            'Dott\.ssa' => 'Dottoressa',
		            'Prof\.' => 'Professore',
		            'Prof\.ssa' => 'Professoressa',
		            'etc\.' => 'et cetera .',
		            '%' => 'per cento'
		            };
	$ab{'GERMAN'} = {
		            'Hr\.' => 'Herr',
		            'Fr\.' => 'Frau',
		            'Frl\.' => 'Fraulein',
		            'Dr\.' => 'Doktor',
		            'Prof\.' => 'Professor',
		            'etc\.' => 'et cetera .',
		            '%' => 'Prozente'
		            };
	$ab{'FRENCH'} = {
		            'M\.' => 'Monsieur',
		            'Mme' => 'Madame',
		            'Mlle' => 'Mademoiselle',
		            'Dr\.' => 'Docteur',
		            'Prof\.' => 'Professeur',
		            'etc\.' => 'et cetera .',
		            '%' => 'pour cent',
		            'c. - à-d\.?' =>  "c'est-à-dire"
		            };
	
	foreach my $k (keys(%{$ab{$lang}})) {
		$text =~ s/$k/$ab{$lang}{$k}/g;
	}
	return $text;
}





while (<>) {
#    $_ = Encode::decode( 'utf8', $_);

	chomp;
	while ($_ =~ s/\([^\(]*?\)//g) {};

	next if $_ =~ /<.*?>/;
	next if $_ =~ /^$/;

	$_ = abbrev($_);
	
	#remove hyphens
	sub g {
		my $x = shift;
		$x =~ s/-/ /g;
		return $x;
	}
	s/\.-/ . /g;
	s/(^| )([[:alnum:]]{2,}(?:\-[[:alnum:]]{2,})+)(?= |\n|'s|$)/$1.g($2)/ge;
	s/(^| )-([[:alnum:]]+)(?= |\n|'s|$)/$1$2/g;
	s/(^| )([[:alpha:]]+)-( |\n|'s|$)/$1$2$3/g;
	
	#split acronyms
	s/' ([st]) /'$1 /g;
	s/ ([LltmsS]) ' / $1' /g;
	s/(^| )([A-Z])(?=[0-9])/$1$2\. /g;
	s/([0-9])([A-Z])(?= |\n|'s|$)/$1 $2\./g;
	s/([0-9]+(?:[,\.][0-9]+)?)/ $1 /g;
	
	#numbers
	s/(^| )([0-9]+(?:[,\.][0-9]+)?)(?= |\n|'s|$)/$1.num2str($2)/ge;
	
	#end of acronyms
	sub f {
		my $x = shift;
		$x =~ s/\./ /g;
		$x =~ s/-/ /g;
		$x =~ s/([A-Z])/ $1./g;
		return $x;
	}
	s/(^| )((?:[A-Z]-?\.?){2,})(?= |\n|'s|$)/$1.f($2)/ge;
	s/(^| )([B-DF-HJ-NP-TVWXZ])(?= |\n|'s|$)/$1$2\./g;
	s/(^| )([A-Z])-(?= |\n|'s|$)/$1$2\./g;
	
	
	s/  +/ /g;
	s/^ //gm;
	s/ $//gm;
	
	my @line = ();
	foreach my $w (split(/ +/, $_)) {
		if ($w =~ /^[\.!\?\n]+$/) {
			if ($g_no_line_seg == 0) {
				if (@line+0 > 0) {
					$output .= join(" ", @line)."\n";
				}
				@line = ();
			}
		}
		elsif ($w =~ /^[^[:alnum:]]$/) {
			next;
		}
		else {
			$w =~ 
			push(@line, $w);
		}
	}
	if (@line+0 > 0) {
		$output .= join(" ", @line)."\n";
	}


	if ($lang eq "FRENCH") {
		$output =~ s/ á / à /gi;
		$output =~ s/-á-/-à-/gi;
		$output =~ s/^a /à /gim;
		$output =~ s/quelqu' un /quelqu'un /gi;
		$output =~ s/c' qu/ce qu/gi;
		$output =~ s/c' /c'/gi;
		$output =~ s/s' est/s'est/gi;
		$output =~ s/s' agit /s'agit /gi;
		$output =~ s/s' agir/s'agir/gi;
		$output =~ s/s' agiss/s'agiss/gi;
		$output =~ s/s' il /s'il /gi;
		$output =~ s/s' ils /s'ils /gi;
		$output =~ s/d' abord /d'abord /gi;
		$output =~ s/(^| )d un(e?) /$1d'un$2 /gi;
		$output =~ s/(^| )([jl])' ai /$1$2'ai /gi;
		$output =~ s/(^| )([jl])' y /$1$2'y /gi;
		$output =~ s/(^| )([ltm])' a /$1$2'a /gi;
		$output =~ s/(^| )n' est /$1n'est /gi;
		$output =~ s/(^| )n' a /$1n'a /gi;
		$output =~ s/(^| )([djlmnst])' y /$1$2'y /gi;
		$output =~ s/(^| )([cdjlmnst])' en /$1$2'en /gi;
		$output =~ s/(^| )(qu)' y /$1$2'y /gi;
		$output =~ s/(^| )(qu)' en /$1$2'en /gi;
		$output =~ s/-t-(il|elle|on)/ -t-$1/gi;
	}
	elsif ($lang eq "ENGLISH") {
		$output =~ s/(^| )(I|he|she|we|you|they) '(ll|d) /$1$2'$3 /gi;
		$output =~ s/(^| )(I|we|you|they) 've /$1$2've /gi;
		$output =~ s/(^| )I 'm /$1I'm /gi;
		$output =~ s/(^| )(he|she|there) 's /$1$2's /gi;
		$output =~ s/(^| )(we|you|they) 're /$1$2'm /gi;
	}
	elsif ($lang eq "ITALIAN") {
		$output =~ s/(^| )(un|quest)'/$1$2' /gi;
	}
	elsif ($lang eq "SPANISH") {
#		$output =~ s/ EE\.UU\.? / E. E. U. U. /g;
	}	
	
	$output =~ s/ '([st])( |$)/'$1$2/g;
	$output =~ s/F\. I\. F\. A\./FIFA/gm;
	$output =~ s/ÖVP/Ö. V. P./gm;
	$output =~ s/FPÖ/F. P. Ö./gm;
}

#remove greek letters appart if $lang==greek
if ($lang ne "GREEK") {
	$output =~ s/[^\p{InBasic_Latin}\p{InLatin-1_Supplement}\d\.\'\-\n]/ /g;
}
else {
	$output =~ s/[^\P{greek}\w\d\.\'\-]/ /g;
}
$output =~ s/(^| )([\w\d\'\-]{2,})\./$1$2 /g;
$output =~ s/([^\w])\./$1 /g;

$output =~ s/  +/ /g;
$output =~ s/^ //gm;
$output =~ s/ $//gm;


#$output = encode_utf8($output);
print $output;



#while (<>) {
#
#	
#}

