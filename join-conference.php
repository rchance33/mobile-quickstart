<?php
	//$conferenceName = $_REQUEST["ConferenceName"];
	$conferenceName = 'Room1';
    header('Content-type: text/xml');
?>

<Response>
	<Say>Joining Conference <?php echo $conferenceName;?></Say>
	<Dial>
		<Conference><?php echo $conferenceName;?></Conference>
	</Dial>
</Response>