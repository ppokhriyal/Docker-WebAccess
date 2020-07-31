/* Show Table Pagination */

$(document).ready(function(){
		$('#imagetable').DataTable({
			"pagingType": "full_numbers",
			"ordering": false
		});
		$('.dataTables_length').addClass('bs-select');
	});