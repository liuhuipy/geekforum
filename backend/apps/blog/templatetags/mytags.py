__author__ = 'liuhui'

from django import template


register = template.Library()


@register.assignment_tag
def pagination(page_obj, paginator, num_of_displaypages=11,num_of_backpages=5):
    num_of_frontpages = num_of_backpages
    html = ''

    if paginator.num_pages <= num_of_displaypages + num_of_backpages:
        for page_num in range(1, paginator.num_pages+1):
            html += '<li><a href="?page=%s">%s</a></li>' % (page_num, page_num)
        return html
    elif page_obj.number <= num_of_displaypages - num_of_backpages + 2:
        for page_num in range(1, num_of_displaypages + 1):
            html += '<li><a href="?page=%s">%s</a></li>' % (page_num, page_num)
        html += '''
            <li class="disabled"><a href="?page=%s">...</a></li>
            <li><a href="?page=%s">%s</a></li>
        ''' % (paginator.num_pages,paginator.num_pages,paginator.num_pages)
        return html
    elif num_of_displaypages - num_of_backpages +2 < page_obj.number <= paginator.num_pages - num_of_backpages -2:
        html = '''
            <li><a href="?page=1">1</a></li>
            <li class="disabled"><a href="?page=1">...</a></li>
        '''
        for i in range(page_obj.number - num_of_frontpages, page_obj.number + num_of_backpages + 1):
            html += '<li><a href="?page=%s">%s</a></li>' % (i, i)
        html += '''
            <li class="disabled"><a href="?page=%s">...</a></li>
            <li><a href="?page=%s">%s</a></li>
        ''' % (paginator.num_pages,paginator.num_pages,paginator.num_pages)
        return html
    else:
        html = '''
            <li><a href="?page=1">1</a></li>
            <li class="disabled"><a href="?page=1">...</a></li>
        '''
        for i in range(page_obj.number - num_of_frontpages, paginator.num_pages+1):
            html += '<li><a href="?page=%s">%s</a></li>' % (i, i)
        return html



