(function($) {

    $(document).ready(function () {
        $.getJSON("https://api.github.com/repos/cherdon/ForeDoc/commits", function(data){
            var date = data[0].commit.committer.date.split("T")[0];
            var sha = data[0].sha;
            $(".copy").text("Copyright © 2020 Fore. Publication Date: " + date );
            $(".copy").wrap('<a href="https://github.com/cherdon/ForeDoc/commit/' + sha + '" target="_blank" />')
          });
     });

})(jQuery);