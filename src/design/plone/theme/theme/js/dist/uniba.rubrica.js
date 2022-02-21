// eslint-disable-next-line no-undef
requirejs(
  [
    'jquery',
    'https://static.ict.uniba.it/uniba.widgets/rubrica/handlebars.min.js',
  ],
  function($, Handlebars) {
    'use scrict';

    function getQueryVariables(url) {
      var varsFound = {};
      var query = url.split('/')[url.split('/').length - 1];
      query =
        query.indexOf('?') > -1 ? query.substring(query.indexOf('?') + 1) : '';
      var vars = query.split('&');
      for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        varsFound[pair[0]] = pair[1] ? pair[1] : '';
      }
      return varsFound;
    }

    var appRubrica = {
      jsonUrlHost: 'https://persone.ict.uniba.it',
      entityList: {
        username: { template: '' },
        docente: { template: '' },
      },
      srcPath: 'https://static.ict.uniba.it/uniba.widgets/rubrica/',
      cssSelector: 'external-link',
      rubricaNodes: {},

      init: function() {
        var scripts = document.querySelectorAll('script');
        Array.prototype.forEach.call(scripts, function(el) {
          if (el.src.indexOf('uniba.rubrica.js') > -1) {
            //el.src.substring(0, currentsrc);
            appRubrica.cssSelector =
              getQueryVariables(el.src)['selector'] !== undefined
                ? getQueryVariables(el.src)['selector']
                : appRubrica.cssSelector;
            return;
          }
        });

        // appRubrica.initHandlebarsLib();
        appRubrica.interceptSnippets();

        var stylefile = document.createElement('link');
        stylefile.setAttribute('rel', 'stylesheet');
        stylefile.setAttribute('type', 'text/css');
        stylefile.setAttribute(
          'href',
          appRubrica.srcPath + 'uniba.rubrica.css'
        );
        document.getElementsByTagName('head')[0].appendChild(stylefile);
      },
      initHandlebarsLib: function() {
        // inizializzo la libreria
        var handlebarsScript = 'handlebars.min.js';
        var handlebarsScriptNode = document.createElement('script');
        handlebarsScriptNode.setAttribute(
          'src',
          appRubrica.srcPath + handlebarsScript
        );
        if (typeof Handlebars == 'undefined') {
          document
            .getElementsByTagName('head')[0]
            .appendChild(handlebarsScriptNode);
        }
      },
      templatesHtml: function() {
        // ottengo i template per le varie entita' disponibili

        for (var entTemplate in appRubrica.entityList) {
          var req = new XMLHttpRequest();
          req.open('GET', appRubrica.srcPath + entTemplate + '.hbs.html', true);
          //iniettiamo nella request il template che utilizzeremo dopo
          req.template = entTemplate;
          req.onload = function() {
            if (this.status >= 200 && this.status < 400) {
              // prendiamo dalla request (this) il template iniettato prima
              var desumeEntity = this.template;
              appRubrica.entityList[desumeEntity].template = this.responseText;
              // faccio partire la callback per renderizzare i template per entita
              if (appRubrica.rubricaNodes[desumeEntity] !== undefined) {
                Array.prototype.forEach.call(
                  appRubrica.rubricaNodes[desumeEntity],
                  function(item) {
                    appRubrica.callPersone({}, item.dataAttributes, item.el);
                  }
                );
              }
            } else {
              console.log('Failed while connecting to the server : ');
              console.log(this);
            }
          };
          req.onerror = function() {
            console.log('Error: Failed while connecting to the server : ');
            console.log(this);
          };
          req.send();
        }
      },
      callbackPersone: function(data, dataAttributes, obj) {
        var entity = dataAttributes['entity'];
        var style = dataAttributes['style']
          ? dataAttributes['style']
          : 'default';
        data['dataAttributes'] = dataAttributes;
        var template = Handlebars.compile(
          appRubrica.entityList[entity].template
        );
        var putInPlace = document.createElement('div');
        putInPlace.className = 'rubricauniba_wrapper ' + entity + ' ' + style;

        //HELPERS
        Handlebars.registerHelper('formatPhone', function(phone, options) {
          if (phone) {
            var arrayPhone = phone.split(':');
            return arrayPhone[0];
          }
          return options.inverse(this);
        });
        // verifico la possibilita' di inserire il testo del tag di anchor nel nuovo div che conterra' i dati
        var objHTML =
          dataAttributes['showText'] && dataAttributes['showText'] == '1'
            ? '<p>' + obj.innerHTML + '</p>'
            : '';
        // preparo contenuto del div di rubrica
        putInPlace.innerHTML = objHTML + template(data);
        putInPlace.className = 'rubricauniba ' + putInPlace.className;
        try {
          obj.parentNode.insertBefore(putInPlace, obj.nextSibling);
          obj.parentNode.removeChild(obj);
        } catch (err) {
          // errore
        }
      },
      interceptSnippets: function() {
        // intercetto ed elaboro i nodi che rappresentano placeholder di Rubrica
        var rubricaAnchor = document.querySelectorAll(
          '.' +
            appRubrica.cssSelector +
            '[href^="' +
            appRubrica.jsonUrlHost +
            '"][href*="json"]'
        );
        //var rubricaAnchor = document.querySelectorAll('.'+appRubrica.cssSelector+'[href^="'+appRubrica.jsonUrlHost+'"]');

        // ciclo sui nodi che dovrebbero contenere dati di rubrica
        Array.prototype.forEach.call(rubricaAnchor, function(el) {
          // elaboro il nodo di template handlebars da mettere nel placeholder
          var dataAttributes = {};
          var destUrl =
            el.getAttribute('href') &&
            el.getAttribute('href').indexOf(appRubrica.jsonUrlHost) > -1
              ? el.getAttribute('href')
              : undefined;
          var destUrlArray =
            destUrl != undefined ? destUrl.split('/') : undefined;
          dataAttributes =
            destUrl != undefined ? getQueryVariables(destUrl) : {};
          //dataAttributes['entity'] = destUrl!=undefined ? destUrlArray[destUrlArray.length-2] : undefined;
          dataAttributes['entity'] =
            destUrl != undefined ? 'username' : undefined;
          // testo se fare override del template handlebars
          dataAttributes['entity'] =
            dataAttributes['template'] !== undefined &&
            appRubrica.entityList[dataAttributes['template']] !== undefined
              ? dataAttributes['template']
              : dataAttributes['entity'];
          dataAttributes['id'] =
            destUrl != undefined
              ? destUrlArray[destUrlArray.length - 1]
              : undefined;
          dataAttributes['url'] = destUrl != undefined ? destUrl : undefined;
          if (destUrl != undefined) {
            //VITO appRubrica.callPersone({},dataAttributes, el);
            if (
              appRubrica.rubricaNodes[dataAttributes['entity']] === undefined
            ) {
              appRubrica.rubricaNodes[dataAttributes['entity']] = [];
            }
            appRubrica.rubricaNodes[
              dataAttributes['entity']
            ] = appRubrica.rubricaNodes[dataAttributes['entity']].concat({
              el: el,
              dataAttributes: dataAttributes,
            });
          }
        });
        // carico i template grafici handlebars
        appRubrica.templatesHtml();
      },
      callPersone: function(sendData, dataAttributes, cbObj) {
        var req = new XMLHttpRequest();
        var jsonurl = dataAttributes['url'];

        req.open('GET', jsonurl, true);
        req.onload = function() {
          if (this.status >= 200 && this.status < 400) {
            // Success!
            if (this.responseText != '') {
              appRubrica.callbackPersone(
                JSON.parse(this.responseText),
                dataAttributes,
                cbObj
              );
            }
          } else {
            console.log('Failed while connecting to the server');
          }
        };

        req.onerror = function() {
          console.log('Failed while connecting to the server');
        };

        req.send();
      },
    };

    $(document).ready(function() {
      appRubrica.init();
    });
  }
);
