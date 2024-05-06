use strict;

my $motifDir = "/content/drive/MyDrive/deeptfni/data_resource/human_HOCOMO/";
opendir (DIR,"$motifDir") || die "Error";
my @file = grep {/meme/}readdir(DIR);
closedir (DIR);
my %motif;
my $n;
foreach my $m(@file){
	my $name = (split /_/,$m)[0];
	$motif{$name} = 1;
	$n++;
}
#print "total TF motif: $n\n";
print STDERR 'total TF motif: $n\n';

open (f1,"/content/drive/MyDrive/deeptfni/data_resource/gencode.v19.ProteinCoding_gene_promoter.txt") || die "Error";
open (o1,">/content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.temp") || die "Error";
my $n;
while (<f1>)
{
	$_=~s/\s+$//;
	my @a = split /\t/,$_;
	next if $motif{$a[-1]} eq "";
	$n++;
	print o1 "$_\n";
}
close f1;
close o1;
print STDERR 'TF motif in gencode19: $n\n';
system ("/content/drive/MyDrive/deeptfni/bedops/bin/sort-bed /content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.temp > /content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.txt");
#sort_bed("/content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.temp", "/content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.txt");
system ("rm /content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.temp");

my $input = $ARGV[0];
my $input_dir = "/content/drive/MyDrive/deeptfni/${input}_data/";
my $dir = "/content/drive/MyDrive/deeptfni/TFBS_region/";
my $outtemp = "/content/drive/MyDrive/deeptfni/data_resource/bedops_temp/";
mkdir $outtemp unless -e $outtemp;
system ("/content/drive/MyDrive/deeptfni/bedops/bin/bedops -e -100% $dir$input.txt /content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.txt > $outtemp$input.txt");# unless -e "$outtemp$input.txt"
my $n = count("$outtemp$input.txt");
print STDERR "TFBS in TF promoter: $n\n";

my %hash;
my %val;
open (f1,"/content/drive/MyDrive/deeptfni/data_resource/gencode.v19.TF.promoter.txt") || die "Error";
my $tempCount;
while (<f1>)
{
	$_=~s/\s+$//;
	print "read $tempCount\n" if $tempCount%100 == 0;
  
	$tempCount++;
	my @a = split /\t/,$_;
	my ($chr,$start,$end,$TF) = ($a[0],$a[1],$a[2],$a[4]);
	open (f2,"$outtemp$input.txt") || die "Error";
	my $sum;
	while (<f2>)
	{
		$_=~s/\s+$//;
		my @a = split /\t/,$_;
		next if $a[0] ne $chr;
		if ($a[1] >= $start && $a[2] <= $end){
			my $p = join "\t",$TF,$a[3];
			my $q = join "\t",$a[3],$TF;
			$hash{$p} = 1;$hash{$q} = 1;
			$sum++;
		}
	}
	close f2;
	$val{$TF} = 1 if $sum > 0;
}
close f1;
my $n = scalar(keys %val);
print STDERR "val TF number: $n\n";
my $outdir = "/content/drive/MyDrive/deeptfni/Adjacency_matrix";
mkdir $outdir unless -e $outdir;
open (o1,">$outdir/$input.txt") || die "Error";
open (o2,">$outdir/$input.TF.list.txt") || die "Error";
print o1 "TF";
foreach my $m(keys %val){print o1 "\t$m";}
print o1 "\n";
my $sum;
foreach my $m(keys %val){
	print o1 "$m";
	print o2 "$m\n";
	foreach my $n(keys %val){
		my $p = join "\t",$m,$n;
    system ("python log_data.py $p");
		$hash{$p} = 0 if $hash{$p} eq "";
		$sum+=$hash{$p};
		print o1 "\t$hash{$p}";
	}
	print o1 "\n";
}
close o1;
my $density = sprintf("%.2f",$sum/scalar(keys %val)/scalar(keys %val));
print STDERR "$input density:$sum\t$density\n";


my $out_dir = "/content/drive/MyDrive/deeptfni/$input/";
mkdir $out_dir unless -e $out_dir;
my $input_file = "$input_dir$input.csv";
print ("input_file = $input_file\n");
system ("python /content/drive/MyDrive/deeptfni/6_dense_matrix_2_h5_for_MAESTRO_input.py -sample $input -input_file $input_file -output_dir $out_dir");

sub count{
	my @a = @_;
	my $n;
	open (f1,"$a[0]") || die "Error $a[0]";
	while (<f1>){$n++;}
	close f1;
	return $n;
}

## Subroutine to sort BED file
#sub sort_bed {
#  my ($input_file, $output_file) = @_;
#
#  open(my $fh_in, "<", $input_file) or die "Error: $!";
#  open(my $fh_out, ">", $output_file) or die "Error: $!";
#
#  my @lines = <$fh_in>;
#  my @sorted_lines = sort { my ($chr1, $start1) = (split /\t/, $a)[0,1]; my ($chr2, $start2) = (split /\t/, $b)[0,1]; $chr1 cmp $chr2 || $start1 <=> $start2 } @lines;
#
#  print $fh_out @sorted_lines;
#
#  close $fh_in;
#  close $fh_out;
#}
