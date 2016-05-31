var hourglass = {

    statusclasses: {
        'OK': 'success',
        'Warning': 'warning',
        'Critical': 'danger'
    },

    statusnames: {
        0: 'OK',
        1: 'Warning',
        2: 'Critical'
    },

    addFormGroup: function(name, filter=null) {
        if (filter === null) {
            filter = name;
        }
        formitem = $('<select multiple class="ms" data-name="'+name+'" data-filter="'+filter+'" class="form-control" id="'+name+'-filter"><select>').appendTo( $('#'+name+'-filter-div') );
    },

}

String.prototype.capitalize = function(all) {
    if (all) {
        return this.split(' ').map(function(i) {
            return i.capitalize()
        }).join(' ');
    } else {
        return this.charAt(0).toUpperCase() + this.slice(1);
    }
}

$(document).ready(function() {
    (function($) {
        $.QueryString = (function(a) {
            if (a == "") return {};
            var b = {};
            for (var i = 0; i < a.length; ++i)
            {
                var p=a[i].split('=');
                if (p.length != 2) continue;
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
            }
            return b;
        })(window.location.search.substr(1).split('&'))
    })(jQuery);
});