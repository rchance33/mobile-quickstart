<?php 
require "Services/Twilio/Capability.php";

$accountSid = "ACf820f938c757753436311d289f1918b3"; 
$authToken = "f57f92a9db4d9f4845bf917b36c30e49";

// The app outgoing connections will use: 
$appSid = "APb7372771a18a38669a83e5f115dabeb8";

$capability = new Services_Twilio_Capability($accountSid, $authToken);

// This would allow outgoing connections to $appSid: 
if($_REQUEST['allowOutgoing'] != 'false')
    $capability->allowClientOutgoing($appSid);

if($_REQUEST['client'] != null)
    $capability->allowClientIncoming("mobile-quickstart4");
// This would return a token to use with Twilio based on // the account and capabilities defined above 
$token = $capability->generateToken();

echo $token; 

?>