/*
 * File: app/store/gridOutputs.js
 * Date: Wed Sep 04 2013 17:44:34 GMT+0200 (CEST)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.store.gridOutputs', {
    extend: 'Ext.data.Store',

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'gridoutputs',
            proxy: {
                type: 'ajax',
                reader: {
                    type: 'json',
                    idProperty: 'definition',
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
                    name: 'definition',
                    type: 'string'
                },
                {
                    name: 'uom',
                    type: 'string'
                },
                {
                    name: 'value',
                    type: 'string'
                },
                {
                    name: 'role'
                },
                {
                    name: 'from',
                    type: 'string'
                },
                {
                    name: 'to',
                    type: 'string'
                },
                {
                    name: 'list',
                    type: 'string'
                },
                {
                    name: 'ctype'
                }
            ]
        }, cfg)]);
    }
});