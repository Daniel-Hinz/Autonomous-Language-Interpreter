<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <title>ALI</title>
  <meta name="description" content="A simple HTML5 Template for new projects.">
  <meta name="author" content="SitePoint">

  <meta property="og:title" content="A Basic HTML5 Template">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.sitepoint.com/a-basic-html5-template/">
  <meta property="og:description" content="A simple HTML5 Template for new projects.">
  <meta property="og:image" content="image.png">

  <link rel="shortcut icon" type="image/x-icon" href="static\images\icon.ico">  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <link rel="stylesheet" href="static/css/home-page.css">

  <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300&amp;display=swap" rel="stylesheet">
</head>

<body>
    <nav class="navbar">
        <div class="logo">ALI</div>

        <ul>
          <li><a href="#">Translator</a></li>
          <li><a href="#">Text to Speech</a></li>
          <li><a href="#">Previous Entries</a></li>
          <li><a href="#">My Profile</a></li>
        </ul>

        <div class="hamburger">
            <div class="hamburger-line"></div>
            <div class="hamburger-line"></div>
            <div class="hamburger-line"></div>
        </div>
    </nav>

    <div class="links"> 
      <div class="exit-wrapper"><i class="fas fa-times link-close"></i></div>
      <div class="link">Translator<i class="fas fa-chevron-right"></i></div>
      <div class="link">Text to Speech<i class="fas fa-chevron-right"></i></div>
      <div class="link">Previous Entries<i class="fas fa-chevron-right"></i></div>
      <div class="link">My Profile<i class="fas fa-chevron-right"></i></div>
    </div>

    <div class="mic-wrapper">
      <i class="fas fa-microphone"></i>
    </div>

    <h2>Press and hold to translate.</h2>

    <div class="lang-wrapper">
      <select name="cars" id="cars">
        <option value="">Select Language</option>
        <option value="af">Afrikaans</option>
        <option value="sq">Albanian</option>
        <option value="am">Amharic</option>
        <option value="ar">Arabic</option>
        <option value="hy">Armenian</option>
        <option value="az">Azerbaijani</option>
        <option value="eu">Basque</option>
        <option value="be">Belarusian</option>
        <option value="bn">Bengali</option>
        <option value="bs">Bosnian</option>
        <option value="bg">Bulgarian</option>
        <option value="ca">Catalan</option>
        <!-- add more -->
        
      </select>
    </div>

    <div class="translation-tab">View Text</div>

    <div class="text-wrapper">
      <textarea class="translation" placeholder="View recorded speech here..."></textarea>
      <i class="fas fa-exchange-alt"></i>
      <textarea class="translation" placeholder="View translated speech here..."></textarea>
      <i class="fas fa-times text-close"></i>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.js"
            integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk="
            crossorigin="anonymous">
    </script>
    <script src="static/scripts/home-page-js"></script>
</body>
</html>