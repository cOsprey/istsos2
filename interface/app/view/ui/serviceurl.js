/*
 * File: app/view/ui/serviceurl.js
 * Date: Wed Sep 04 2013 17:44:34 GMT+0200 (CEST)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.view.ui.serviceurl', {
    extend: 'Ext.form.Panel',

    border: 0,
    bodyPadding: 10,
    title: '',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'fieldset',
                    padding: 10,
                    checkboxName: 'cbproxy',
                    title: 'Proxy url',
                    items: [
                        {
                            xtype: 'textfield',
                            name: 'url',
                            fieldLabel: 'Url',
                            allowBlank: false,
                            anchor: '100%'
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }
});