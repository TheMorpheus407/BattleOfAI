$(document).ready(function () {
    let footer = $("footer")[0];
    footer.classList.add("page-footer");
    footer.classList.add("red");
    footer.classList.add("darken-2");
    footer.innerHTML = '\
    <div class="container">\
        <div class="row">\
            <div class="col s12" id="extras">\
            </div>\
            <div class="col right right-align">\
                <h5>Battle of AI</h5>\
                <p>Problems? Suggestions? Contact me.</p>\
                <div class="footer-social-links">\
                    <a href="https://www.youtube.com/subscription_center?add_user=TheMorpheus407" class="linkedin"><i class="fab fa-youtube"></i></a>\
                    <a href="https://twitter.com/TheMorpheusTuts" class="twitter"><i class="fab fa-twitter"></i></a>\
                    <a href="https://www.facebook.com/themorpheustutorials" class="facebook"><i class="fab fa-facebook"></i></a>\
                    <a href="https://github.com/TheMorpheus407" class="instagram"><i class="fab fa-github"></i></a>\
                    <a href="https://www.patreon.com/user?u=5322110" class="google-plus"><i class="fab fa-patreon"></i></a>\
                    <a href="https://discord.gg/xW7k3xd" class="google-plus"><i class="fab fa-discord"></i></a>\
                    <a href="http://amzn.to/2slBSgH" class="google-plus"><i class="fab fa-amazon"></i></a>\
                    <a href="https://www.paypal.me/TheMorpheus" class="google-plus"><i class="fab fa-paypal"></i></a>\
                </div>\
            </div>\
        </div>\
        <div class="footer-copyright row red darken-3">\
            <div class="container col s12">\
                © 2018 The Morpheus Tutorials\
                <a href="terms.html" class="offset-terms right white-text">Terms of Use</a>\
                <a href="privacypolicy.html" class="right white-text">Privacy Policy</a>\
            </div>\
        </div>\
    </div>\
    ';
});