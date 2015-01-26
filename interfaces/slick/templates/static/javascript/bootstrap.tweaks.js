//define the onclick event for the menu
$(".menuLink").on('click', function (e) {

	//Set active menu item, first remove active status for the currently selected menu item
	$(this).parent().parent().find('.active').removeClass('active');
	$('.nav').find('.active').removeClass('active');

	//Then set the current menu item to acive
	$(this).parent().addClass('active');

	//Disable the link action, so nothing else happens when the menu is selected
	e.preventDefault(); // stops link from loading

	//Hide all existing page content
	$('.content').hide();

	//Then show the content for the current selected menu item get the href and use it find which div to show
	$($(this).attr('href')).show();

});