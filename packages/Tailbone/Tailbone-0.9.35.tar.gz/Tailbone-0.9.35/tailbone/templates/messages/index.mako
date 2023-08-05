## -*- coding: utf-8; -*-
<%inherit file="/master/index.mako" />

<%def name="context_menu_items()">
  % if request.has_perm('messages.create'):
      <li>${h.link_to("Send a new Message", url('messages.create'))}</li>
  % endif
</%def>

<%def name="grid_tools()">
  % if request.matched_route.name in ('messages.inbox', 'messages.archive'):
      ${h.form(url('messages.move_bulk'), **{'@submit': 'moveMessagesSubmit'})}
      ${h.csrf_token(request)}
      ${h.hidden('destination', value='archive' if request.matched_route.name == 'messages.inbox' else 'inbox')}
      ${h.hidden('uuids', v_model='selected_uuids')}
      <b-button type="is-primary"
                native-type="submit"
                :disabled="moveMessagesSubmitting || !checkedRows.length">
        {{ moveMessagesTextCurrent }}
      </b-button>
      ${h.end_form()}
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  % if request.matched_route.name in ('messages.inbox', 'messages.archive'):
      <script type="text/javascript">

        TailboneGridData.moveMessagesSubmitting = false
        TailboneGridData.moveMessagesText = null

        TailboneGrid.computed.moveMessagesTextCurrent = function() {
            if (this.moveMessagesText) {
                return this.moveMessagesText
            }
            let count = this.checkedRows.length
            return "Move " + count.toString() + " selected to ${'Archive' if request.matched_route.name == 'messages.inbox' else 'Inbox'}"
        }

        TailboneGrid.methods.moveMessagesSubmit = function() {
            this.moveMessagesSubmitting = true
            this.moveMessagesText = "Working, please wait..."
        }

      </script>
  % endif
</%def>


${parent.body()}
