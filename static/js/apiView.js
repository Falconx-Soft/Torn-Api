console.log("***********")
$(document).ready(function () {
	$('#dtBasicExample').DataTable();
	$('#min, #max').keyup( function() {
        table.draw();
    } );

  });

var table = $('#dtBasicExample').DataTable({ "paging": true , 
  "searching":true,
   responsive: true,
   "paging": false,
});

console.log(table)
$('#date_status').on( 'change', function () {
	console.log(this.value)
	table
		.column( 1 )
		.search( this.value )
		.draw();
} );

$('#date_name').on( 'change', function () {
	console.log(this.value)
	table
		.column( 0 )
		.search( this.value )
		.draw();
} );

$('#date_faction').on( 'change',function () {
	console.log(this.value)
	table
		.column( 5 )
		.search( this.value )
		.draw();
} );

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseInt( $('#min').val(), 10 );
        var max = parseInt( $('#max').val(), 10 );
        var stats = parseInt( data[6] ) || 0; // use data for the stats column
 
        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && stats <= max ) ||
             ( min <= stats   && isNaN( max ) ) ||
             ( min <= stats   && stats <= max ) )
        {
            return true;
        }
        return false;
    }
);

document.getElementById("dtBasicExample_filter").style.display="none";

document.getElementById("dtBasicExample_info").style.display="none";