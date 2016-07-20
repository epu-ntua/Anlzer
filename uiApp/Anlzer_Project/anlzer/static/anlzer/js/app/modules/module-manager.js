/**
 * Created by DarkA_000 on 3/31/2016.
 */

(function(exports) {
    var fns = [];
    
    exports.add = function(fn) {
        fns.push(fn);
        return exports
    };

    exports.call = function() {
        for (var i = 0; i < fns.length; i++) {
            fns[i]();
        }
        return fns;
    }
})(this.moduleManager = {});
