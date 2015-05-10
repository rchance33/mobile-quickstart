<?php 
require "Services/Twilio/Capability.php";

$accountSid = "AC4cbe7e3cb0b70ab1eb2e5ccf81005c71"; 
$authToken = "b0ccc8c0fcb902a9531482c9e8911fac";

// The app outgoing connections will use: 
$appSid = "APb7372771a18a38669a83e5f115dabeb8";

$capability = new Services_Twilio_Capability($accountSid, $authToken);

// This would allow outgoing connections to $appSid: 
if($_REQUEST['allowOutgoing'] != 'false')
    $capability->allowClientOutgoing($appSid);

if($_REQUEST['client'] != null)
    $capability->allowClientIncoming($appSid);
// This would return a token to use with Twilio based on // the account and capabilities defined above 
$token = $capability->generateToken();

echo $token; 

?>