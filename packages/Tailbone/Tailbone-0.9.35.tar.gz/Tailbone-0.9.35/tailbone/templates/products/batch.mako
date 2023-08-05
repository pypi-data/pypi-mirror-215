## -*- coding: utf-8; -*-
<%inherit file="/form.mako" />

<%def name="title()">Create Batch</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Back to Products", url('products'))}</li>
</%def>

<%def name="render_deform_field(form, field)">
  <b-field horizontal
           % if field.description:
           message="${field.description}"
           % endif
           % if field.error:
           type="is-danger"
           :message='${form.messages_json(field.error.messages())|n}'
           % endif
           label="${field.title}">
    ${field.serialize()|n}
  </b-field>
</%def>

<%def name="render_form_innards()">
  ${h.form(request.current_route_url(), **{'@submit': 'submit{}'.format(form.component_studly)})}
  ${h.csrf_token(request)}

  <section>
    ${render_deform_field(form, dform['batch_type'])}
    ${render_deform_field(form, dform['description'])}
    ${render_deform_field(form, dform['notes'])}

    % for key, pform in six.iteritems(params_forms):
        <div v-show="field_model_batch_type == '${key}'">
          % for field in pform.make_deform_form():
              ${render_deform_field(pform, field)}
          % endfor
        </div>
    % endfor
  </section>

  <br />
  <div class="buttons">
    <b-button type="is-primary"
              native-type="submit"
              :disabled="${form.component_studly}Submitting">
      {{ ${form.component_studly}ButtonText }}
    </b-button>
    <b-button tag="a" href="${url('products')}">
      Cancel
    </b-button>
  </div>

  ${h.end_form()}
</%def>

<%def name="render_form()">
  <script type="text/x-template" id="${form.component}-template">
    ${self.render_form_innards()}
  </script>
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ## TODO: ugh, an awful lot of duplicated code here (from /forms/deform_buefy.mako)

    let ${form.component_studly} = {
        template: '#${form.component}-template',
        methods: {

            ## TODO: deprecate / remove the latter option here
            % if form.auto_disable_save or form.auto_disable:
                submit${form.component_studly}() {
                    this.${form.component_studly}Submitting = true
                    this.${form.component_studly}ButtonText = "Working, please wait..."
                }
            % endif
        }
    }

    let ${form.component_studly}Data = {

        ## TODO: ugh, this seems pretty hacky.  need to declare some data models
        ## for various field components to bind to...
        % if not form.readonly:
            % for field in form.fields:
                % if field in dform:
                    <% field = dform[field] %>
                    field_model_${field.name}: ${form.get_vuejs_model_value(field)|n},
                % endif
            % endfor
        % endif

        ## TODO: deprecate / remove the latter option here
        % if form.auto_disable_save or form.auto_disable:
            ${form.component_studly}Submitting: false,
            ${form.component_studly}ButtonText: ${json.dumps(getattr(form, 'submit_label', getattr(form, 'save_label', "Submit")))|n},
        % endif

        ## TODO: more hackiness, this is for the sake of batch params
        ## (this of course was *not* copied from normal deform template!)
        % for key, pform in params_forms.items():
            <% pdform = pform.make_deform_form() %>
            % for field in pform.fields:
                % if field in pdform:
                    <% field = pdform[field] %>
                    field_model_${field.name}: ${pform.get_vuejs_model_value(field)|n},
                % endif
            % endfor
        % endfor
    }

  </script>
</%def>


${parent.body()}
