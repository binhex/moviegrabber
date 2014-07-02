function checkbox_checked(queue_release_checkbox_id,queue_purge_checkbox_id)
	{
	if (document.getElementById(queue_release_checkbox_id).checked == true)
		{
		document.getElementById(queue_purge_checkbox_id).checked = true;	
		}
	else
		{
		document.getElementById(queue_purge_checkbox_id).checked = false;
		}
	}
