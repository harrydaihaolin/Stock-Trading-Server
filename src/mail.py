import logging
logging = logging.getLogger()
import constants
from mailchimp3 import MailChimp
import web_template
from string import Template

client = MailChimp(mc_api=constants.MAILCHIMPAPI, mc_user=constants.MAILCHIMPUSENAME)
campaign_name="trading_alert"
from_name="Haolin Dai"
reply_to="harry442930583@gmail.com"
audience_id="4e7840abaf" 

def getAudiencesId():
    try:
        return client.lists.all(get_all=True, fields="lists.name,lists.id")
    except Exception as e:
        logging.error(e)

def campaign_creation_function(campaign_name, audience_id, from_name, reply_to, client=client):
    campaign_name = campaign_name
    audience_id = audience_id
    from_name = from_name
    reply_to = reply_to

    data = {
        "recipients" :
        {
            "list_id": audience_id
        },
        "settings":
        {
            "subject_line": campaign_name,
            "from_name": from_name,
            "reply_to": reply_to
        },
        "type": "regular"
    }

    new_campaign = client.campaigns.create(data=data)
    
    return new_campaign

def customized_template(html_code, campaign_id, client=client):
    html_code = html_code
    campaign_id = campaign_id
    string_template = Template(html_code).safe_substitute()
    
    try:
        client.campaigns.content.update(
                campaign_id=campaign_id,
                data={'message': 'Campaign message', 'html': string_template}
                )
    except Exception as error:
        logging.error(error)


def send_mail(client=client):      
    campaign = campaign_creation_function(campaign_name, audience_id, from_name, reply_to)
    campaign_id = campaign['id']
    try:
        customized_template(web_template.html_code, campaign_id)
        client.campaigns.actions.send(campaign_id=campaign_id)
    except Exception as error:
        logging.error(error)

