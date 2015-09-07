/**
 * http://silktide.com/cookieconsent
 * 
 * BBB: we added also a "reject" button feature here, but it's disabled.
 * BBB: note we are also using jQuery here. That's a mixed way to do things
 */

(function ($) {
  // Stop from running again, if accidently included more than once.

  if (window.hasCookieConsent) return;
  window.hasCookieConsent = true;

  var portal_url = window.portal_url || '';

  /*
   Constants
   */

  // Client variable which may be present containing options to override with
  var OPTIONS_VARIABLE = 'cookieconsent_options';

  // Name of cookie to be set when policy is accepted of rejected
  var DISMISSED_COOKIE = 'cookieconsent';

  // The path to built in themes (s3 bucket)
  var THEME_BUCKET_PATH = 'http://cc.silktide.com/';

  // The DOM Script that host banner JSON configuration
  var BANNER_CONF_ID = 'cookieconsent-banner-configuration';
  var RESET_OPTOUT_COOKIES_VIEW = '@@reset-optout';

  // No point going further if they've already dismissed.
  if (document.cookie.indexOf(DISMISSED_COOKIE) > -1) {
    return;
  }

  // rer.cookieconsent structures, inited after DOM load below
  var bannerConfiguration = null,
      bannerRawConf,
      currentLanguage = null,
      $labelsElement = null
      cookie_consent_configuration = null;

  // IE8...
  if(typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function() {
      return this.replace(/^\s+|\s+$/g, '');
    };
  }

  /*
   Helper methods
   */
  var Util = {
    isArray: function (obj) {
      var proto = Object.prototype.toString.call(obj);
      return proto == '[object Array]';
    },

    isObject: function (obj) {
      return Object.prototype.toString.call(obj) == '[object Object]';
    },

    each: function (arr, callback, /* optional: */context, force) {
      if (Util.isObject(arr) && !force) {
        for (var key in arr) {
          if (arr.hasOwnProperty(key)) {
            callback.call(context, arr[key], key, arr);
          }
        }
      } else {
        for (var i = 0, ii = arr.length; i < ii; i++) {
          callback.call(context, arr[i], i, arr);
        }
      }
    },

    merge: function (obj1, obj2) {
      if (!obj1) return;
      Util.each(obj2, function (val, key) {
        if (Util.isObject(val) && Util.isObject(obj1[key])) {
          Util.merge(obj1[key], val);
        } else {
          obj1[key] = val;
        }
      });
    },

    bind: function (func, context) {
      return function () {
        return func.apply(context, arguments);
      };
    },

    /*
     find a property based on a . separated path.
     i.e. queryObject({details: {name: 'Adam'}}, 'details.name') // -> 'Adam'
     returns null if not found
     */
    queryObject: function (object, query) {
      var queryPart;
      var i = 0;
      var head = object;
      query = query.split('.');
      while ( (queryPart = query[i++]) && head.hasOwnProperty(queryPart) && (head = head[queryPart]) )  {
        if (i === query.length) return head;
      }
      return null;
    },

    setCookie: function (name, value, expirydays) {
      var exdate = new Date();
      expirydays = expirydays || 365;
      exdate.setDate(exdate.getDate() + expirydays);
      document.cookie = name + '=' + value + '; expires=' + exdate.toUTCString() + '; path='
        + (bannerConfiguration.portal_path ? bannerConfiguration.portal_path : '/');
    },

    addEventListener: function (el, event, eventListener) {
      if (el.addEventListener) {
        el.addEventListener(event, eventListener);
      } else {
        el.attachEvent('on' + event, eventListener);
      }
    }
  };

  var DomBuilder = (function () {
    /*
     The attribute we store events in.
     */
    var eventAttribute = 'data-cc-event';
    var conditionAttribute = 'data-cc-if';

    /*
     Shim to make addEventListener work correctly with IE.
     */
    var addEventListener = function (el, event, eventListener) {
      // Add multiple event listeners at once if array is passed.
      if (Util.isArray(event)) {
        return Util.each(event, function (ev) {
          addEventListener(el, ev, eventListener);
        });
      }

      if (el.addEventListener) {
        el.addEventListener(event, eventListener);
      } else {
        el.attachEvent('on' + event, eventListener);
      }
    };

    /*
     Replace {{variable.name}} with it's property on the scope
     Also supports {{variable.name || another.name || 'string'}}
     */
    var insertReplacements = function (htmlStr, scope) {
      return htmlStr.replace(/\{\{(.*?)\}\}/g, function (_match, sub) {
        var tokens = sub.split('||');
        var value;
        while (token = tokens.shift()) {
          token = token.trim();

          // If string
          if (token[0] === '"') return token.slice(1, token.length - 1);

          // If query matches
          value =  Util.queryObject(scope, token);

          if (value) return value;
        }

        return '';
      });
    };

    /*
     Turn a string of html into DOM
     */
    var buildDom = function (htmlStr) {
      var container = document.createElement('div');
      container.innerHTML = htmlStr;
      return container.children[0];
    };

    var applyToElementsWithAttribute = function (dom, attribute, func) {
      var els = dom.parentNode.querySelectorAll('[' + attribute + ']');
      Util.each(els, function (element) {
        var attributeVal = element.getAttribute(attribute);
        func(element, attributeVal);
      }, window, true);
    };

    /*
     Parse event attributes in dom and set listeners to their matching scope methods
     */
    var applyEvents = function (dom, scope) {
      applyToElementsWithAttribute(dom, eventAttribute, function (element, attributeVal) {
        var parts = attributeVal.split(':');
        var listener = Util.queryObject(scope, parts[1]);
        addEventListener(element, parts[0], Util.bind(listener, scope));
      });
    };

    var applyConditionals = function (dom, scope) {
      applyToElementsWithAttribute(dom, conditionAttribute, function (element, attributeVal) {
        var value = Util.queryObject(scope, attributeVal);
        if (!value) {
          element.parentNode.removeChild(element);
        }
      });
    };

    return {
      build: function (htmlStr, scope) {
        if (Util.isArray(htmlStr)) htmlStr = htmlStr.join('');

        htmlStr = insertReplacements(htmlStr, scope);
        var dom = buildDom(htmlStr);
        applyEvents(dom, scope);
        applyConditionals(dom, scope);

        return dom;
      }
    };
  })();


  /*
   Plugin
   */
  var cookieconsent = {
    options: {
      message: 'This website uses cookies to ensure you get the best experience on our website. ',
      dismiss: 'Got it!',
      learnMore: 'More info',
      link: null,
      container: null, // selector
      theme: 'light-floating'
    },

    init: function () {
      var options = window[OPTIONS_VARIABLE];
      if (options) this.setOptions(options);
      this.setContainer();

      // Calls render when theme is loaded.
      if (this.options.theme) {
        this.loadTheme(this.render);
      } else {
        this.render();
      }
    },

    setOptions: function (options) {
      Util.merge(this.options, options);
    },

    setContainer: function () {
      if (this.options.container) {
        this.container = document.querySelector(this.options.container);
      } else {
        this.container = document.body;
      }

      // Add class to container classes so we can specify css for IE8 only.
      this.containerClasses = '';
      if (navigator.appVersion.indexOf('MSIE 8') > -1) {
        this.containerClasses += ' cc_ie8'
      }
    },

    loadTheme: function (callback) {
      var theme = this.options.theme;

      // If theme is specified by name
      if (theme.indexOf('.css') === -1) {
        theme = THEME_BUCKET_PATH + theme + '.css';
      }

      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.type = 'text/css';
      link.href = theme;

      var loaded = false;
      link.onload = Util.bind(function () {
        if (!loaded && callback) {
          callback.call(this);
          loaded = true;
        }
      }, this);

      document.getElementsByTagName("head")[0].appendChild(link);
    },

    markup: [
      '<div class="cc_banner-wrapper {{containerClasses}}" aria-live="assertive" role="alert">',
        '<div class="cc_banner cc_container cc_container--open">',
          '<p class="cc_message">{{options.message}}</p>',
          '<div class="btn_container">',
            '<a id="accept_btn" href="{{options.accept_url}}" data-cc-event="click:accept" class="cc_btn cc_btn_accept_all">{{options.accept}}</a>',
//            '<a id="reject_btn" href="{{options.reject_url}}" data-cc-event="click:reject" class="cc_btn cc_btn_accept_all">{{options.reject}}</a>',
          '</div>',
        '</div>',
      '</div>'
    ],

    // '<p class="cc_message">{{options.message}} <a data-cc-if="options.link" class="cc_more_info" href="{{options.link || "#null"}}">{{options.learnMore}}</a></p>'

    render: function () {
      this.element = DomBuilder.build(this.markup, this);
      if (!this.container.firstChild) {
        this.container.appendChild(this.element);
      } else {
        this.container.insertBefore(this.element, this.container.firstChild);
      }
    },

    accept: function () {
      this.setDismissedCookie('true');
      this.container.removeChild(this.element);
    },

    reject: function () {
      this.setDismissedCookie('false');
      this.container.removeChild(this.element);
    },

    setDismissedCookie: function (value) {
      Util.setCookie(DISMISSED_COOKIE, value);
    }
  };

  var initialized = false;
  var init = function () {
    if (!initialized && document.readyState == 'interactive') {

      // IE is not able to read script content as simple text
      bannerRawConf = $('#' + BANNER_CONF_ID).text() || $('#' + BANNER_CONF_ID).html();
      bannerConfiguration = $.parseJSON(bannerRawConf);

      if (!bannerConfiguration || bannerConfiguration.cookie_consent_configuration.length===0) {
        // No configuration provided: no output
        return;
      }

      currentLanguage = $('html').attr('lang') || 'en';
      $labelsElement = $($('#cookieconsent-banner-configuration-label').text());

      // Now load the "right" configuration: take the one for the current language or the first (default) ones
      for (var i=0;i<bannerConfiguration.cookie_consent_configuration.length; i++) {
        if (bannerConfiguration.cookie_consent_configuration[i].lang===currentLanguage) {
          cookie_consent_configuration = bannerConfiguration.cookie_consent_configuration[i];
          break;
        }
      }
      if (!cookie_consent_configuration) {
        cookie_consent_configuration = bannerConfiguration.cookie_consent_configuration[0];
      }

      window.cookieconsent_options = {
        message: cookie_consent_configuration.text,
        accept: $labelsElement.find('accept').text(),
        reject: $labelsElement.find('reject').text(),
        accept_url: bannerConfiguration.here_url
          ? (bannerConfiguration.here_url + '/' + RESET_OPTOUT_COOKIES_VIEW + '?came_from=' + bannerConfiguration.actual_url)
          : 'javascript:void(0)',
        reject_url: 'javascript:void(0)',
        learnMore: 'Privacy policy',
        link: portal_url + '/privacy',
        theme: portal_url + '/++resource++rer.cookieconsent.resources/cookiepolicy.css'
      };

      // Events for automatic policy acceptance
      if (bannerConfiguration.accept_on_click) {
        function forcePolicyAcceptance(ev) {
          // Prevent accepting policy if we want to read the policy or access the dashboard
          if (this.tagName.toLowerCase()==='a') {
            if (this.href.indexOf(cookie_consent_configuration.privacy_link_url) === 0 ||
                this.href.indexOf(bannerConfiguration.dashboard_url) === 0) {
              return;
            }
          }
          cookieconsent.accept();
          this.href += '/@@reset-optout';
        }
        $('a:not(.cc_banner-wrapper a)').click(forcePolicyAcceptance);
        $('form:not(#optout-form)').submit(forcePolicyAcceptance);
      }

      cookieconsent.init();
      initalized = true;
    }
  };

  $(document).ready(init);

})(jQuery);
