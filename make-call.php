<?php
	// A phone number you have previously validated with Twilio
    $twilioPhoneNumber = $_REQUEST['From'];
	
	// If the number above isn't changed, send an error immediately.
	//if ( $twilioPhoneNumber == 'XXXXXXXXXX' )
//	{
//		header("Must replace caller ID phone number with an authenticated Twilio number", TRUE, -500);
//		return;
//	}
    
	// Include the Twilio PHP library
    require 'Services/Twilio.php';
 
    // Twilio REST API version
    $version = "2010-04-01";
 
    // Set our Account SID and AuthToken
    $acctSid = 'AC4cbe7e3cb0b70ab1eb2e5ccf81005c71';
    $authToken = 'b0ccc8c0fcb902a9531482c9e8911fac';
        
    //Initalize the response URL
    $url = "http://mobile-quickstart4.herokuapp.com/join-conference.php";
     
    //HTTP Request the participants array passed in the URL
 	//$participants = $_REQUEST['participants']; 
    $participants = array($_REQUEST['To'], $_REQUEST['From']);
     
    // Instantiate a new Twilio Rest Client
    $client = new Services_Twilio($acctSid, $authToken, $version);
 	
	foreach ($participants as $participant)
	{
		//Make REST call for each participant
		try 
		{	
			// Initiate a new outbound call to either a Phone Number or 
			// Client.  It's expected that a Client call will have "client:"
			// prepended to the $participant string by the invoker of this 
			// make-call.php URL.
			$call = $client->account->calls->create(
						$twilioPhoneNumber, // The number of the phone initiating the call
						$participant, // The number or client name of the phone or device receiving call
						$url //The URL with the TwimL that will be executed
					);
		  echo 'Started call: ' . $call->sid;
		}
		catch (Exception $e) 
		{
			echo 'Error: ' . $e->getMessage();
		}
	}
?>