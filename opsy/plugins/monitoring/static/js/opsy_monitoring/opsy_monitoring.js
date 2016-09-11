var opsy_monitoring = {

  statusclasses: {
    'Ok': 'success',
    'Warning': 'warning',
    'Critical': 'danger'
  },

  statusnames: {
    0: 'OK',
    1: 'Warning',
    2: 'Critical'
  },

  addFormGroup: function(name, filter) {
    if (filter === undefined) {
      filter = name;
    }
    formitem = $('<select multiple class="ms" data-name="' + name +
      '" data-filter="' + filter + '" class="form-control" id="' + name +
      '-filter"><select>').appendTo($('#' + name + '-filter-div'));
  },

  getDashboardUrl: function(url) {
    dash = $.QueryString.dashboard;
    if (dash) {
      var separator = url.indexOf('?') !== -1 ? '&' : '?';
      return url + separator + 'dashboard=' + dash;
    } else {
      return url;
    }
  },

  checkZones: function() {
    $.getJSON('/api/monitoring/zones', function(json) {
      zones = json.zones;
      for (var i = 0; i < zones.length; i++) {
        zone = zones[i];
        if (zone.status != 'ok') {
          opsy.notification.add(zone.name + ' Poller Failure', 'Datacenter ' +
            zone.name + ' is not responding!', 'danger', zone.name +
            '-offline');
        } else {
          opsy.notification.remove(zone.name + '-offline');
        }
      }
    });
  },

  multiselectOptions: {
    buttonWidth: '100%',
    enableFiltering: true,
    enableCaseInsensitiveFiltering: true,
    numberDisplayed: 1,
    includeSelectAllOption: true,
    buttonText: function(options, select) {
      if (options.length == 1) {
        return $(options[0]).attr('label');
      } else if (options.length == $(select).children(options).length) {
        return 'All items selected';
      } else if (options.length > 1) {
        return options.length + ' items selected';
      } else {
        return $(select).data('name').replace('-', ' ').capitalize(true);
      }
    },
    buttonTitle: function(options, select) {
      return $(select).data('name').replace('-', ' ').capitalize(true);
    },
    onDropdownHidden: function() {
      events.datatables.updateUrl();
      document.eventstable.ajax.reload(null, false);
    },
  }

}