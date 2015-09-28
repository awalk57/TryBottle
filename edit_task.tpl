%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected URLDB item
<p>Edit the task with ID = {{no}}</p>
<form action="/edit/{{no}}" method="get">
<input type="text" name="task" value="{{old.task}}" size="50" maxlength="50">
<input type="text" name="urlstr" value="{{old.urlstr}}" size="50" maxlength="50">
<input type="text" name="chk_status" value="{{old.chk_status}}" size="5" maxlength="5">
<select name="status">
<option>open</option>
<option>closed</option>
</select>
<br/>
<input type="submit" name="save" value="save">
</form>