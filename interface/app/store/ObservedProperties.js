/*
 * File: app/store/ObservedProperties.js
 * Date: Wed Sep 04 2013 17:44:34 GMT+0200 (CEST)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.store.ObservedProperties', {
    extend: 'Ext.data.Store',

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'observedproperties',
            proxy: {
                type: 'ajax',
                reader: {
                    type: 'json',
                    idProperty: 'definition',
                    messageProperty: 'message',
                    root: 'data'
                }
            },
            fields: [
                {
                    name: 'name',
                    type: 'string'
                },
                {
                    name: 'description',
                    type: 'string'
                },
                {
                    name: 'uom',
                    type: 'string'
                },
                {
                    name: 'definition',
                    type: 'string'
                }
            ]
        }, cfg)]);
    }
});