%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
<p><h3>Your Finished TODO Items:</h3></p>
<table border="1">
%for row in rows:
  <tr>
    <td>{{row.id}}</td>
    <td>{{row.task}}</td>
    <td><a href="/edit/{{row.id}}"> Edit</a></td>
  </tr>
%end
</table>
<p>Create <a href="/new">New</a> item</p>