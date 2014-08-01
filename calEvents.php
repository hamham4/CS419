<?php

# Input Parameters
$givenStartyear = "2014";
$givenStartmonth = "07";
$givenStartday = "31";

$givenEndyear = "2014";
$givenEndmonth = "08";
$givenEndday = "01";

$givenStartDate = $givenStartyear . $givenStartmonth . $givenStartday;
$givenEndDate = $givenEndyear . $givenEndmonth . $givenEndday;

$userName = "cs419.team4";


$urlBegin = "https://www.google.com/calendar/feeds/";
$urlEnd = "%40gmail.com/public/basic";

$calURl = $urlBegin . $userName . $urlEnd;

$calendarURL = trim($calURl);
if (strpos($calendarURL, "basic")) {
    $calendarURL = ereg_replace("basic", "full", $calURl);
}

$dateformat = "j F Y"; // 1 June 2014
$timeformat = "g:i A"; // 12:34 AM
?>

<?php
$confirmed = 'http://schemas.google.com/g/2005#event.confirmed';

// Get 12 hour period
$one_day_in_seconds = 60 * 60 * 24;
$startDay = date("Y-m-d\Th:i:sP", strtotime($givenStartDate));
$endDay = date("Y-m-d\Th:i:sP", (strtotime($givenEndDate) + $one_day_in_seconds));

$feed = $calendarURL . "?orderby=starttime&singleevents=true&" .
  "start-min=" . $startDay . "&" . "start-max=" . $endDay;

$doc = new DOMDocument();
$doc->load($feed);

$entries = $doc->getElementsByTagName("entry");

$meta_box = array('fields'=>array());
$fields = &$meta_box['fields'];

foreach ($entries as $entry) {

    $status = $entry->getElementsByTagName("eventStatus");
    $eventStatus = $status->item(0)->getAttributeNode("value")->value;

    if ($eventStatus == $confirmed) {
        $titles = $entry->getElementsByTagName("title");
        $title = $titles->item(0)->nodeValue;

        $contents = $entry->getElementsByTagName("content");
        $content = $contents->item(0)->nodeValue;

        $times = $entry->getElementsByTagName("when");
        $startTime = $times->item(0)->getAttributeNode("startTime")->value;
        $when = date("l jS F Y - h:i A", strtotime($startTime));

        $endTime = $times->item(0)->getAttributeNode("endTime")->value;
		
        $googleCalDate = date($dateformat, strtotime($startTime));
        $googleCalDateStart = date($dateformat, strtotime($startTime));
        $googleCalDateEnd = date($dateformat, strtotime($endTime));
        $googleCalStartTime = date($timeformat, strtotime($startTime));
        $googleCalEndTime = date($timeformat, strtotime($endTime));
        $googleCalMonthStart = date("F", strtotime($startTime));
        $googleCalYearStart = date("Y", strtotime($startTime));
        $googleCalDayStart = date("j", strtotime($startTime));        

        $places = $entry->getElementsByTagName("where");
        $where = $places->item(0)->getAttributeNode("valueString")->value;

    }
	
	$arr = array($googleCalYearStart, $googleCalMonthStart, $googleCalDayStart, $googleCalStartTime, $googleCalEndTime);

	echo json_encode($arr);
	echo "<br/>";
	
	$fields[] = array($googleCalYearStart, $googleCalMonthStart, $googleCalDayStart, $googleCalStartTime, $googleCalEndTime);
	
// 	$file = fopen('results.json', 'w+');
// 	#fwrite($file, json_encode($arr));
// 	
// 	$file = file_get_contents('results.json');
// 	$data = json_decode($file);
// 	unset($file);//prevent memory leaks for large json.
// 	//insert data here
// 	$data[] = array($googleCalYearStart, $googleCalMonthStart, $googleCalDayStart, $googleCalStartTime, $googleCalEndTime);
// 	//save the file
// 	file_put_contents('results.json',json_encode($data));
// 	unset($data);//release memory
// 	
}

	$file = fopen('results.json', 'w+');
	#fwrite($file, json_encode($arr));
	
	$file = file_get_contents('results.json');
	$data = json_decode($file);
	unset($file);//prevent memory leaks for large json.
	//insert data here
	$data[] = $fields;
	//save the file
	file_put_contents('results.json',json_encode($data));
	unset($data);//release memory
	

?>

