function dynamic_dropdown(post_config_dropdown1_id,post_config_dropdown2_id) 
	{
	var dropdown1 = document.getElementById(post_config_dropdown1_id);
	var dropdown1_value = dropdown1.options[dropdown1.selectedIndex].value;

	var dropdown2 = document.getElementById(post_config_dropdown2_id);
	var dropdown2_value = dropdown2.options[dropdown2.selectedIndex].value;

	if (dropdown1_value == "filename") {
	dropdown2.options.add(new Option("equal to"));
	dropdown2.options.add(new Option("not equal to"));	
	}

	if (dropdown1_value == "extension") {
		selbox.options[selbox.options.length] = new
		Option('equal to','extension_equal_to');
		selbox.options[selbox.options.length] = new
		Option('not equal to','extension_not_equal_to');
	}

	if (dropdown1_value == "size") {
		selbox.options[selbox.options.length] = new
		Option('equal to','size_equal_to');
		selbox.options[selbox.options.length] = new
		Option('not equal to','size_not_equal_to');
		selbox.options[selbox.options.length] = new
		Option('greater than','size_greater_than');
		selbox.options[selbox.options.length] = new
		Option('less than','size_less_than');
	}

	if (dropdown1_value == "genre") {
		selbox.options[selbox.options.length] = new
		Option('equal to','genre_equal_to');
		selbox.options[selbox.options.length] = new
		Option('not equal to','genre_not_equal_to');
	}

	if (dropdown1_value == "certificate") {
		selbox.options[selbox.options.length] = new
		Option('equal to','certificate_equal_to');
		selbox.options[selbox.options.length] = new
		Option('not equal to','certificate_not_equal_to');
		selbox.options[selbox.options.length] = new
		Option('greater than','certificate_greater_than');
		selbox.options[selbox.options.length] = new
		Option('less than','certificate_less_than');
	}
	
	}