use strict;

my $outdir = "/content/drive/MyDrive/deeptfni/TFBS_region/";
mkdir $outdir unless -e $outdir;
print STDERR "EXECUTING 4-TFBS_REGIONS";

my $dataset = $ARGV[0];
{
	print "dataset : $dataset\n";
	my $dir = "/content/drive/MyDrive/deeptfni/fimo-res/$dataset.clean.ATAC_peak_1e4/";
	opendir (DIR,"$dir") || die "Error";
	my @file = grep {/txt/}readdir (DIR);
	closedir (DIR);

	open (o1,">$outdir$dataset.temp") || die "Error";
	my $fn;
	foreach my $m(@file)
	{
		my $name = (split /\.txt/,$m)[0];
    print STDERR $name;
		open (f1,"$dir$m") || die "Error";
		open (o2,">$dir$name.temp") || die "Error";
		while (<f1>)
		{
			$_=~s/\s+$//;
			last if($_ eq '');
			my @a = split /\t/,$_;
			next if $a[0] =~ /motif_id/;
			if ($a[7] > 1e-6){next;}
			my $tf = (split /_/,$a[0])[0];
      print STDERR "extracted TF: $tf\n";
			my ($chr, $start, $end) = split /-/,$a[2],3;
      print STDERR "($chr, $start, $end)\n";

			($start, $end) = ($start+$a[3]-1, $start+$a[4] - 1);
			print o1 "$chr\t$start\t$end\t$tf\n";
			print o2 "$chr\t$start\t$end\t$tf\n";
		}
		close f1;
		close o2;
		system ("/content/drive/MyDrive/deeptfni/bedops/bin/sort-bed $dir$name.temp > $dir$name.bed");
    print STDERR "got bed files\n";
    #sort_bed("$dir$name.temp", "$dir$name.bed");
		system ("rm $dir$name.temp");
	}
	close o1;

	system ("/content/drive/MyDrive/deeptfni/bedops/bin/sort-bed $outdir$dataset.temp > $outdir$dataset.txt");
  #sort_bed("$outdir$dataset.temp", "$outdir$dataset.txt");
	system ("rm $outdir$dataset.temp");
	print STDERR "run adjance matrix construction\n";
	system ("perl /content/drive/MyDrive/deeptfni/5-GetMatrix.pl $dataset");
}


## Subroutine to sort BED file
#sub sort_bed {
#    my ($input_file, $output_file) = @_;
#
#    open(my $fh_in, "<", $input_file) or die "Error: $!";
#    open(my $fh_out, ">", $output_file) or die "Error: $!";
#
#    my @lines = <$fh_in>;
#    my @sorted_lines = sort { my ($chr1, $start1) = (split /\t/, $a)[0,1]; my ($chr2, $start2) = (split /\t/, $b)[0,1]; $chr1 cmp $chr2 || $start1 <=> $start2 } @lines;
#
#    print $fh_out @sorted_lines;
#
#    close $fh_in;
#    close $fh_out;
#}
