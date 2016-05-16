// Makerspace Card System
// Stand and mount for swipe-out panel
// Print the stand and mount separately.
// The printable implementations of the models are at the bottom of the file.

// Hardware dimensions
screw_d = 5;

// Base dimensions
base_l = 190;
base_w = 120;
base_t = 6;

// Column dimensions
col_d = 25;
col_h = 80;
col_offset = col_h/2 + base_t/2;

// Mount dimensions
mount_angle = 25;
mount_l = 55;
mount_w = 55;
mount_t = 6;
mount_form_t = mount_t*3;
mount_offset = col_h + base_t - 10;

// Nub dimensions
nub_l = 10;
nub_w = 5;
nub_t = 5;

// Explosion factor
e_factor = 0;

// Mount module
module mount()
{
	difference()
	{
		cube([mount_l,mount_w,mount_t], center=true);
		for(i=[-20,20])
			translate([i,0,0]) cylinder(d=screw_d,h=mount_t+2, center=true);
	}	
	translate([0,-10,-mount_t/2+nub_t/2-2])
		cube([nub_l,nub_w,nub_t], center=true);

}

// Mount form for trimming the column
module mount_form()
{
	translate([0,0,mount_form_t/2-mount_t/2])
		cube([mount_l-1,mount_w-1,mount_form_t], center=true);
	cylinder(d=screw_d,h=60, center=true); // hole for screw
	translate([0,0,-15]) hull()
	{
		translate([0,0,0]) cylinder(d=screw_d*2,h=screw_d,center=true); //space for nut
		translate([0,7,0]) cylinder(d=screw_d*2,h=screw_d,center=true); //space for nut
	}
	translate([0,-10,-mount_t+nub_t/2-1])
			cube([nub_l,nub_w,nub_t], center=true);

}

// Base module
module base()
{
	translate([0,-10,0])
		cube([base_l,base_w,base_t], center=true);
}

module curved_base()
{
	translate([0,-32,0])
	difference()
	{
		scale([1.7,.9,1])
			cylinder(d=base_l,h=base_t, center=true);
		translate([0,-base_w/3,0])
			scale([1.4,.9,1.2])
				cylinder(d=base_l,h=base_t, center=true);
	}	
}

// Column module
module column()
{
	translate([0,0,col_offset])
		cylinder(d=col_d,h=col_h, center=true);
}

// Demonstrate stand model
module exploded_demo()
{
	rotate([mount_angle,0,0])
	{
		translate([0,0,e_factor]) 
			difference() // mount
			{
				mount();
				cylinder(d=screw_d,h=50, center=true); // arbitrary length; hole for screw
				translate([0,0,-mount_t/4]) cylinder(d=screw_d*2,h=mount_t); // for screw head
			}
		translate([0,-10,mount_t/2+1+e_factor*2])
		{
			%cube([200,150,2], center=true); // panel model; use % in front to make translucent
			translate([50,-120,0]) cube([2,90,10], center=true);
		}
	}
	difference() // base + column - mount_form
	{
		translate([0,0,-mount_offset]) 
		{
			column();
			base();
		}
		rotate([mount_angle,0,0])
			mount_form();
	}
}

// Final Models
module final_mount()
{
	difference() // mount
	{
		mount();
		cylinder(d=screw_d,h=50, center=true); // arbitrary length; hole for screw
		translate([0,0,-mount_t/4]) cylinder(d=screw_d*2,h=mount_t); // for screw head
	}
}

module final_stand()
{
	difference() // base + column - mount_form
	{
		translate([0,0,-mount_offset]) 
		{
			column();
			base();
		}
		rotate([mount_angle,0,0])
			mount_form();
	}
}


// Place things to print here
//final_stand();
final_mount();
